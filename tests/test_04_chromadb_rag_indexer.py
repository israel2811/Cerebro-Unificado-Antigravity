import os
import sys
import tempfile
import unittest
import importlib.util
from unittest.mock import MagicMock, patch

# Ensure chromadb is mocked in sys.modules prior to loading the script module
mock_chromadb = MagicMock()
mock_embedding_functions = MagicMock()
mock_chromadb.utils.embedding_functions = mock_embedding_functions
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = mock_embedding_functions

# Dynamically import 04_chromadb_rag_indexer.py
script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
)
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)


class TestChromaDBIndexerOptimization(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.chunks_dir = os.path.join(self.test_dir.name, "clean_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    def tearDown(self):
        self.test_dir.cleanup()

    @patch.object(indexer_module, 'CLEAN_CHUNKS_DIR')
    def test_indexer_batching_and_sorting(self, mock_clean_chunks_dir):
        # Setup 25 dummy chunk files to test batching (BATCH_SIZE = 20 -> 2 batches: 20 + 5)
        mock_clean_chunks_dir.__fspath__ = lambda self: self.chunks_dir
        # Point indexer CLEAN_CHUNKS_DIR directly to our temp dir
        indexer_module.CLEAN_CHUNKS_DIR = self.chunks_dir

        for i in range(1, 26):
            # Pad with zeros for clear sorting test
            filename = f"chunk_{i:02d}.txt"
            filepath = os.path.join(self.chunks_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Sample content for chunk {i}")

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client

        indexer_module.local_chroma_rag_inject()

        # Should be called twice: 1 batch of 20, 1 batch of 5
        self.assertEqual(mock_collection.add.call_count, 2)

        first_call_args = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_args['documents']), 20)
        self.assertEqual(first_call_args['documents'][0], "Sample content for chunk 1")

        second_call_args = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_args['documents']), 5)
        self.assertEqual(second_call_args['documents'][-1], "Sample content for chunk 25")

    @patch.object(indexer_module, 'CLEAN_CHUNKS_DIR')
    def test_word_truncation_maxsplit(self, mock_clean_chunks_dir):
        indexer_module.CLEAN_CHUNKS_DIR = self.chunks_dir

        # Create a large file with 45,000 words
        large_file = os.path.join(self.chunks_dir, "large_doc.txt")
        words = ["word"] * 45000
        with open(large_file, "w", encoding="utf-8") as f:
            f.write(" ".join(words))

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client

        indexer_module.local_chroma_rag_inject()

        self.assertEqual(mock_collection.add.call_count, 1)
        added_docs = mock_collection.add.call_args[1]['documents']
        # The doc should be truncated to exactly 40,000 words
        truncated_word_count = len(added_docs[0].split())
        self.assertEqual(truncated_word_count, 40000)


if __name__ == "__main__":
    unittest.main()
