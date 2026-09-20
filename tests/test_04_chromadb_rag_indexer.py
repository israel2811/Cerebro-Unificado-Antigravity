import os
import sys
import unittest
import importlib
import importlib.util
from unittest.mock import MagicMock, patch

# Ensure scripts_leviathan is in path
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan"))
sys.path.insert(0, SCRIPTS_DIR)


class TestChromaRAGIndexer(unittest.TestCase):

    def test_word_truncation_logic(self):
        """Test that text exceeding 40,000 words is truncated efficiently using split(None, 40000)."""
        words = ["word"] * 50000
        big_text = " ".join(words)

        split_words = big_text.split(None, 40000)
        self.assertGreater(len(split_words), 40000)

        truncated_text = " ".join(split_words[:40000])
        result_words = truncated_text.split()
        self.assertEqual(len(result_words), 40000)

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("builtins.open")
    def test_local_chroma_rag_inject_batching(self, mock_open, mock_listdir, mock_exists):
        """Test that local_chroma_rag_inject batches collection.add calls in groups of 20."""
        mock_exists.return_value = True

        # Create 25 dummy txt files
        file_list = [f"doc_{i:02d}.txt" for i in range(1, 26)]
        mock_listdir.return_value = file_list

        mock_file_handle = MagicMock()
        mock_file_handle.read.return_value = "This is a short chunk test document."
        mock_open.return_value.__enter__.return_value = mock_file_handle

        mock_collection = MagicMock()
        mock_chroma_client = MagicMock()
        mock_chroma_client.get_or_create_collection.return_value = mock_collection

        # Mock chromadb in sys.modules
        mock_chromadb_module = MagicMock()
        mock_chromadb_module.PersistentClient.return_value = mock_chroma_client

        mock_ef_module = MagicMock()

        with patch.dict("sys.modules", {
            "chromadb": mock_chromadb_module,
            "chromadb.utils": MagicMock(),
            "chromadb.utils.embedding_functions": mock_ef_module,
        }):
            script_path = os.path.join(SCRIPTS_DIR, "04_chromadb_rag_indexer.py")
            spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
            indexer_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(indexer_module)

            indexer_module.local_chroma_rag_inject()

        # Check collection.add calls: 25 files with BATCH_SIZE = 20 -> 2 collection.add calls (20 and 5)
        self.assertEqual(mock_collection.add.call_count, 2)

        # First call should have 20 items
        first_call_kwargs = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_kwargs["documents"]), 20)
        self.assertEqual(len(first_call_kwargs["ids"]), 20)

        # Second call should have remaining 5 items
        second_call_kwargs = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_kwargs["documents"]), 5)
        self.assertEqual(len(second_call_kwargs["ids"]), 5)


if __name__ == "__main__":
    unittest.main()
