import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure mock for chromadb is registered before importing script if chromadb is missing
mock_chroma = MagicMock()
sys.modules['chromadb'] = mock_chroma
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

# Dynamically import the script using importlib since name has numeric prefix
import importlib.util
script_path = os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("rag_indexer", script_path)
rag_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag_indexer)


class TestChromaDBIndexerOptimization(unittest.TestCase):

    def test_maxsplit_truncation_logic(self):
        """Verify that split(None, 40001) correctly truncates texts exceeding 40,000 words."""
        large_text = ("word " * 50000).strip()  # 50,000 words exactly
        words = large_text.split(None, 40001)

        self.assertGreater(len(words), 40000)
        # When splitting with maxsplit=40001, we get 40001 split words plus 1 remainder tail string
        self.assertEqual(len(words), 40002)

        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    def test_maxsplit_normal_text(self):
        """Verify that normal text under 40,000 words is preserved as-is."""
        normal_text = "Hello world from Antigravity Core."
        words = normal_text.split(None, 40001)
        self.assertEqual(len(words), 5)
        self.assertEqual(words, ["Hello", "world", "from", "Antigravity", "Core."])

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="Sample document content for vector database.")
    def test_local_chroma_rag_inject_batching(self, mock_file, mock_listdir, mock_exists):
        """Verify that local_chroma_rag_inject batches collection.add calls in groups of BATCH_SIZE."""
        mock_exists.return_value = True
        # Generate 45 dummy files to test batching (should produce 2 batches of 20 + 1 batch of 5)
        dummy_files = [f"chunk_{i:02d}.txt" for i in range(1, 46)]
        mock_listdir.return_value = list(dummy_files)

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        with patch.object(rag_indexer.chromadb, "PersistentClient", return_value=mock_client):
            rag_indexer.local_chroma_rag_inject()

        # Should be called 3 times (20 + 20 + 5 = 45 documents)
        self.assertEqual(mock_collection.add.call_count, 3)

        # First call: 20 items
        first_call_args = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_args["documents"]), 20)
        self.assertEqual(len(first_call_args["ids"]), 20)
        self.assertEqual(first_call_args["ids"][0], "chunk_1_chunk_01.txt")

        # Second call: 20 items
        second_call_args = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_args["documents"]), 20)

        # Third call: remaining 5 items
        third_call_args = mock_collection.add.call_args_list[2][1]
        self.assertEqual(len(third_call_args["documents"]), 5)


if __name__ == "__main__":
    unittest.main()
