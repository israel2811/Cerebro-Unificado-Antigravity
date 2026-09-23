import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import importlib.util

# Inject mocks for chromadb before importing the target module
chromadb_mock = MagicMock()
embedding_functions_mock = MagicMock()
sys.modules['chromadb'] = chromadb_mock
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = embedding_functions_mock

# Locate and dynamically load the target script with numeric prefix
script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.abspath(os.path.join(script_dir, "..", "scripts_leviathan", "04_chromadb_rag_indexer.py"))

spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
indexer_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_module
spec.loader.exec_module(indexer_module)

class TestIndexerOptimization(unittest.TestCase):
    def setUp(self):
        # Clear mock history before each test
        chromadb_mock.reset_mock()
        embedding_functions_mock.reset_mock()

    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="word " * 50000)
    def test_word_truncation_large_file(self, mock_open, mock_exists, mock_listdir):
        # Configure directory exists and file search
        mock_exists.return_value = True
        mock_listdir.return_value = ["chunk_b.txt", "chunk_a.txt"] # Unsorted list to verify alphabetical sorting

        # Mock Chroma persistent client and collection
        mock_client = MagicMock()
        chromadb_mock.PersistentClient.return_value = mock_client
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        # Invoke local indexer injection
        indexer_module.local_chroma_rag_inject()

        # Verify call arguments
        calls = mock_collection.add.call_args_list
        self.assertEqual(len(calls), 2)

        # Verification 1: Check that file processing order is alphabetical
        first_call_metadata = calls[0][1]['metadatas'][0]
        self.assertEqual(first_call_metadata['source'], 'chunk_a.txt')

        second_call_metadata = calls[1][1]['metadatas'][0]
        self.assertEqual(second_call_metadata['source'], 'chunk_b.txt')

        # Verification 2: Check word truncation logic (capped exactly at 40000 words)
        first_doc = calls[0][1]['documents'][0]
        word_count = len(first_doc.split())
        self.assertEqual(word_count, 40000)

    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="hello world")
    def test_no_truncation_small_file(self, mock_open, mock_exists, mock_listdir):
        mock_exists.return_value = True
        mock_listdir.return_value = ["small_chunk.txt"]

        mock_client = MagicMock()
        chromadb_mock.PersistentClient.return_value = mock_client
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        indexer_module.local_chroma_rag_inject()

        calls = mock_collection.add.call_args_list
        self.assertEqual(len(calls), 1)
        doc = calls[0][1]['documents'][0]
        self.assertEqual(doc, "hello world")

if __name__ == "__main__":
    unittest.main()
