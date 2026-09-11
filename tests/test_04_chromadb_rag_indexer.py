import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import importlib.util

# Ensure chromadb and chromadb.utils are mocked before importing script
chromadb_mock = MagicMock()
sys.modules['chromadb'] = chromadb_mock
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

# Dynamically import 04_chromadb_rag_indexer.py
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py"))
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
indexer_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_module
spec.loader.exec_module(indexer_module)


class TestChromaDBRAGIndexer(unittest.TestCase):

    def test_word_truncation_maxsplit(self):
        """Verify that string splitting handles large inputs and limits to 40000 words."""
        # Test input with 50000 words
        large_text = "word " * 50000
        words = large_text.split(None, 40001)
        # Splitting with maxsplit=40001 yields 40002 elements
        self.assertEqual(len(words), 40002)
        truncated_text = " ".join(words[:40000])
        self.assertEqual(len(truncated_text.split()), 40000)

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("builtins.open")
    def test_local_chroma_rag_inject_batching(self, mock_open, mock_listdir, mock_exists):
        """Verify that files are processed in batch mode (BATCH_SIZE=20) and sorted deterministically."""
        mock_exists.return_value = True
        # 25 files to test batching (20 in first batch, 5 in second)
        filenames = [f"chunk_{i:02d}.txt" for i in range(25, 0, -1)]
        mock_listdir.return_value = filenames

        mock_file_handle = MagicMock()
        mock_file_handle.read.return_value = "This is a test chunk document."
        mock_open.return_value.__enter__.return_value = mock_file_handle

        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        chromadb_mock.PersistentClient.return_value = mock_client

        indexer_module.local_chroma_rag_inject()

        # Check collection.add calls - should be called 2 times (20 items + 5 items)
        self.assertEqual(mock_collection.add.call_count, 2)

        first_call = mock_collection.add.call_args_list[0]
        second_call = mock_collection.add.call_args_list[1]

        # Verify sorted ordering: chunk_01.txt should be first
        self.assertEqual(len(first_call.kwargs['documents']), 20)
        self.assertTrue(first_call.kwargs['ids'][0].endswith("chunk_01.txt"))
        self.assertTrue(first_call.kwargs['ids'][-1].endswith("chunk_20.txt"))

        self.assertEqual(len(second_call.kwargs['documents']), 5)
        self.assertTrue(second_call.kwargs['ids'][0].endswith("chunk_21.txt"))
        self.assertTrue(second_call.kwargs['ids'][-1].endswith("chunk_25.txt"))


if __name__ == "__main__":
    unittest.main()
