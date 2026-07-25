import sys
import os
import unittest
from unittest.mock import MagicMock, patch, mock_open
import importlib.util

# Ensure sys.path includes the scripts_leviathan directory
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Mock chromadb in sys.modules to prevent real DB interaction
mock_chromadb = MagicMock()
mock_embedding_functions = MagicMock()

sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = mock_embedding_functions

# Now dynamically import the module
module_path = os.path.join(scripts_dir, "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", module_path)
indexer_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_module
spec.loader.exec_module(indexer_module)


class TestChromaDBRagIndexer(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_chromadb.reset_mock()
        mock_embedding_functions.reset_mock()

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_local_chroma_rag_inject_no_files(self, mock_listdir, mock_exists):
        """Test behavior when no files are present in the directory."""
        mock_exists.return_value = True
        mock_listdir.return_value = []

        # Run injection
        indexer_module.local_chroma_rag_inject()

        # Verify chromadb was initialized but no files were processed
        mock_chromadb.PersistentClient.assert_called_once()

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_local_chroma_rag_inject_truncation(self, mock_listdir, mock_exists):
        """Test that huge files are correctly truncated to 40000 words using our optimized split."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["huge_chunk.txt"]

        # Create a content string with 50,000 words
        huge_content = " ".join([f"word_{i}" for i in range(50000)])
        expected_content = " ".join([f"word_{i}" for i in range(40000)])

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # Mock open to return the huge content
        with patch("builtins.open", mock_open(read_data=huge_content)):
            indexer_module.local_chroma_rag_inject()

        # Verify collection.add was called with the truncated expected content
        mock_collection.add.assert_called_once()
        kwargs = mock_collection.add.call_args[1]

        # Verify the text is truncated correctly
        self.assertEqual(len(kwargs["documents"]), 1)
        self.assertEqual(kwargs["documents"][0], expected_content)
        self.assertEqual(len(kwargs["documents"][0].split()), 40000)

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_local_chroma_rag_inject_small_file(self, mock_listdir, mock_exists):
        """Test that small files are not truncated and indexed completely."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["small_chunk.txt"]

        small_content = "some words that are definitely less than forty thousand"

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # Mock open to return the small content
        with patch("builtins.open", mock_open(read_data=small_content)):
            indexer_module.local_chroma_rag_inject()

        # Verify collection.add was called with unmodified small content
        mock_collection.add.assert_called_once()
        kwargs = mock_collection.add.call_args[1]
        self.assertEqual(kwargs["documents"][0], small_content)


if __name__ == "__main__":
    unittest.main()
