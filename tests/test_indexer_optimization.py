import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import importlib.util

# Mock the chromadb and dependency modules to avoid ImportErrors
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

# Load the 04_chromadb_rag_indexer.py module dynamically
module_name = "chromadb_rag_indexer"
script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts_leviathan", "04_chromadb_rag_indexer.py")

spec = importlib.util.spec_from_file_location(module_name, script_path)
indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)

class TestIndexerOptimization(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_truncation_under_limit(self, mock_file, mock_listdir, mock_exists):
        """Test that files with words <= 40000 are not truncated."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["chunk_small.txt"]

        # 100 words (within 40000 word limit)
        small_content = " ".join(["word"] * 100)
        mock_file.return_value.__enter__.return_value.read.return_value = small_content

        # Create mocks for chromadb
        mock_client_instance = MagicMock()
        mock_collection = MagicMock()
        mock_client_instance.get_or_create_collection.return_value = mock_collection

        indexer_module.chromadb.PersistentClient = MagicMock(return_value=mock_client_instance)

        # Run the injector
        indexer_module.local_chroma_rag_inject()

        # Check that collection.add was called with the exact original content
        mock_collection.add.assert_called_once()
        called_kwargs = mock_collection.add.call_args[1]
        self.assertEqual(called_kwargs['documents'], [small_content])
        self.assertEqual(len(called_kwargs['documents'][0].split()), 100)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_truncation_over_limit(self, mock_listdir, mock_exists):
        """Test that files with words > 40000 are truncated to exactly 40000 words."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["chunk_large.txt"]

        # 50000 words (exceeds 40000 limit)
        large_content = " ".join(["word"] * 50000)

        # Custom mock open to handle reading large_content
        m = mock_open(read_data=large_content)

        # Create mocks for chromadb
        mock_client_instance = MagicMock()
        mock_collection = MagicMock()
        mock_client_instance.get_or_create_collection.return_value = mock_collection

        indexer_module.chromadb.PersistentClient = MagicMock(return_value=mock_client_instance)

        with patch('builtins.open', m):
            # Run the injector
            indexer_module.local_chroma_rag_inject()

        # Check that collection.add was called with truncated content (exactly 40000 words)
        mock_collection.add.assert_called_once()
        called_kwargs = mock_collection.add.call_args[1]
        doc_passed = called_kwargs['documents'][0]
        word_count = len(doc_passed.split())
        self.assertEqual(word_count, 40000)

if __name__ == '__main__':
    unittest.main()
