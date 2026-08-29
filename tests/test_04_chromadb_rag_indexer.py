import sys
import os
import unittest
from unittest.mock import MagicMock, patch, mock_open
import importlib

class TestChromaDBRagIndexer(unittest.TestCase):
    def setUp(self):
        # Create mock dependencies for chromadb to avoid importing it during test setup
        self.chromadb_mock = MagicMock()
        self.persistent_client_mock = MagicMock()
        self.chromadb_mock.PersistentClient.return_value = self.persistent_client_mock

        # Mock collection and embedding functions
        self.collection_mock = MagicMock()
        self.persistent_client_mock.get_or_create_collection.return_value = self.collection_mock
        self.embedding_functions_mock = MagicMock()
        self.chromadb_mock.utils.embedding_functions = self.embedding_functions_mock

        # Inject our mocks into sys.modules before importing the target script
        sys.modules['chromadb'] = self.chromadb_mock
        sys.modules['chromadb.utils'] = self.chromadb_mock.utils
        sys.modules['chromadb.utils.embedding_functions'] = self.chromadb_mock.utils.embedding_functions

        # Dynamically import the target script using importlib (since it has a numeric prefix)
        spec = importlib.util.spec_from_file_location(
            "scripts_leviathan.04_chromadb_rag_indexer",
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts_leviathan", "04_chromadb_rag_indexer.py")
        )
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def tearDown(self):
        # Clean up sys.modules
        for key in list(sys.modules.keys()):
            if 'chromadb' in key:
                sys.modules.pop(key, None)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_local_chroma_rag_inject_empty_dir(self, mock_listdir, mock_exists):
        """Test the behavior when the chunks directory exists but is empty."""
        mock_exists.return_value = True
        mock_listdir.return_value = []

        self.module.local_chroma_rag_inject()

        self.persistent_client_mock.get_or_create_collection.assert_called_once_with(
            name="tesis_cca",
            embedding_function=self.embedding_functions_mock.SentenceTransformerEmbeddingFunction()
        )
        self.collection_mock.add.assert_not_called()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_local_chroma_rag_inject_with_files(self, mock_listdir, mock_exists):
        """Test indexing with multiple files to verify alphabetical sorting and batching."""
        mock_exists.return_value = True
        # Provide files in unordered name scheme to check if sorted properly
        mock_listdir.return_value = ["chunk_c.txt", "chunk_a.txt", "chunk_b.txt"]

        # Mock file opening
        contents = {
            os.path.join(self.module.CLEAN_CHUNKS_DIR, "chunk_a.txt"): "Content A",
            os.path.join(self.module.CLEAN_CHUNKS_DIR, "chunk_b.txt"): "Content B",
            os.path.join(self.module.CLEAN_CHUNKS_DIR, "chunk_c.txt"): "Content C",
        }

        def mock_open_file(filepath, mode='r', encoding=None):
            content = contents.get(filepath, "")
            return mock_open(read_data=content).return_value

        # We will capture arguments added to collection.add
        added_batches = []
        def mock_add(**kwargs):
            # Capture copies because the batch lists are cleared in the finally block
            added_batches.append({
                'documents': list(kwargs.get('documents', [])),
                'metadatas': list(kwargs.get('metadatas', [])),
                'ids': list(kwargs.get('ids', []))
            })

        self.collection_mock.add.side_effect = mock_add

        # Set BATCH_SIZE dynamically on the module for testing batch boundaries
        self.module.BATCH_SIZE = 2

        with patch('builtins.open', side_effect=mock_open_file):
            self.module.local_chroma_rag_inject()

        # We had 3 files, BATCH_SIZE is 2. So we expect 2 batches: one with 2 files, one with 1 file.
        self.assertEqual(len(added_batches), 2)

        # First batch should have chunk_a and chunk_b due to alphabetical sorting
        self.assertEqual(added_batches[0]['documents'], ["Content A", "Content B"])
        self.assertEqual(added_batches[0]['ids'], ["chunk_1_chunk_a.txt", "chunk_2_chunk_b.txt"])
        self.assertEqual(added_batches[0]['metadatas'], [
            {"source": "chunk_a.txt", "type": "nexus_chunk"},
            {"source": "chunk_b.txt", "type": "nexus_chunk"}
        ])

        # Second batch should have chunk_c
        self.assertEqual(added_batches[1]['documents'], ["Content C"])
        self.assertEqual(added_batches[1]['ids'], ["chunk_3_chunk_c.txt"])
        self.assertEqual(added_batches[1]['metadatas'], [
            {"source": "chunk_c.txt", "type": "nexus_chunk"}
        ])

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_local_chroma_rag_inject_large_file_truncation(self, mock_listdir, mock_exists):
        """Test optimization and truncation of huge chunks exceeding the token boundary."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["large_chunk.txt"]

        # Document with 45000 words
        large_content = "word " * 45000
        contents = {
            os.path.join(self.module.CLEAN_CHUNKS_DIR, "large_chunk.txt"): large_content
        }

        def mock_open_file(filepath, mode='r', encoding=None):
            content = contents.get(filepath, "")
            return mock_open(read_data=content).return_value

        added_batches = []
        def mock_add(**kwargs):
            added_batches.append({
                'documents': list(kwargs.get('documents', [])),
                'metadatas': list(kwargs.get('metadatas', [])),
                'ids': list(kwargs.get('ids', []))
            })

        self.collection_mock.add.side_effect = mock_add

        with patch('builtins.open', side_effect=mock_open_file):
            self.module.local_chroma_rag_inject()

        self.assertEqual(len(added_batches), 1)
        doc = added_batches[0]['documents'][0]
        word_count = len(doc.split())
        self.assertEqual(word_count, 40000)

if __name__ == "__main__":
    unittest.main()
