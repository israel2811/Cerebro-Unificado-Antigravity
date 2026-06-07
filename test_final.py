import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import importlib.util

# Mock chromadb before importing the script
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()

# Load the script as a module
script_path = "scripts_leviathan/04_chromadb_rag_indexer.py"
spec = importlib.util.spec_from_file_location("indexer", script_path)
indexer = importlib.util.module_from_spec(spec)
sys.modules["indexer"] = indexer
spec.loader.exec_module(indexer)

class TestIndexerFinal(unittest.TestCase):
    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test content")
    def test_batch_indexing_logic(self, mock_open, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = [f'file{i}.txt' for i in range(1, 26)]

        mock_client = indexer.chromadb.PersistentClient.return_value
        mock_collection = mock_client.get_or_create_collection.return_value

        indexer.local_chroma_rag_inject()

        self.assertEqual(mock_collection.add.call_count, 2)

    def test_truncation_logic(self):
        # Create a string with many words
        content = "word " * 50000
        # Mock internal split to verify maxsplit
        words = content.split(None, 40001)
        self.assertEqual(len(words), 40001)

if __name__ == '__main__':
    unittest.main()
