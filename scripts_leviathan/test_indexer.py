import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import importlib.util

# Mock the entire chromadb and sentence-transformers modules before importing the indexer
mock_chromadb = MagicMock()
sys.modules["chromadb"] = mock_chromadb
sys.modules["chromadb.utils"] = MagicMock()
sys.modules["chromadb.utils.embedding_functions"] = MagicMock()

# Dynamic import because of the numeric prefix
def import_indexer():
    spec = importlib.util.spec_from_file_location("indexer", "scripts_leviathan/04_chromadb_rag_indexer.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["indexer"] = module
    spec.loader.exec_module(module)
    return module

class TestIndexer(unittest.TestCase):
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_batching_and_truncation(self, mock_listdir, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ["test1.txt", "test2.txt"]

        # Mock chromadb.PersistentClient
        mock_persistent_client = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_persistent_client

        indexer = import_indexer()

        # We need to mock the 'open' function inside the indexer
        with patch("builtins.open", unittest.mock.mock_open(read_data="word " * 50000)) as mock_file:
            mock_collection = MagicMock()
            mock_persistent_client.get_or_create_collection.return_value = mock_collection

            # Set BATCH_SIZE to 1 to test batching logic quickly
            with patch('indexer.BATCH_SIZE', 1):
                indexer.local_chroma_rag_inject()

            # Verify collection.add was called
            self.assertTrue(mock_collection.add.called)
            # Check if truncation happened (MAX_WORDS is 40000)
            # Since BATCH_SIZE=1, it should be called twice
            self.assertEqual(mock_collection.add.call_count, 2)

            call_args = mock_collection.add.call_args
            doc = call_args.kwargs['documents'][0]
            self.assertEqual(len(doc.split()), 40000)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_batch_cleanup_on_error(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["test1.txt", "test2.txt"]

        # Mock chromadb.PersistentClient
        mock_persistent_client = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_persistent_client

        indexer = import_indexer()

        with patch("builtins.open", unittest.mock.mock_open(read_data="content")):
            mock_collection = MagicMock()
            mock_collection.add.side_effect = Exception("Chroma error")
            mock_persistent_client.get_or_create_collection.return_value = mock_collection

            # Set BATCH_SIZE to 1
            with patch('indexer.BATCH_SIZE', 1):
                indexer.local_chroma_rag_inject()

            # Ensure it tried to add twice (since there are 2 files and BATCH_SIZE is 1)
            self.assertEqual(mock_collection.add.call_count, 2)

if __name__ == "__main__":
    unittest.main()
