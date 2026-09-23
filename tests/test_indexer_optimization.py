import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import importlib.util

# Load module dynamically because of numeric prefix '04_'
script_path = os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", os.path.abspath(script_path))

# Inject mock chromadb into sys.modules before importing module
mock_chromadb = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()

indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)

class TestChromaDBIndexerOptimization(unittest.TestCase):

    def test_word_truncation_logic(self):
        """Verify that split(None, 40001) correctly truncates strings exceeding 40,000 words."""
        # Create a string with 45,000 words
        words_45k = ["word" + str(i) for i in range(45000)]
        large_text = " ".join(words_45k)

        # Apply the exact optimized logic from indexer
        words = large_text.split(None, 40001)
        self.assertTrue(len(words) > 40000)
        truncated = " ".join(words[:40000])

        truncated_words = truncated.split()
        self.assertEqual(len(truncated_words), 40000)
        self.assertEqual(truncated_words[0], "word0")
        self.assertEqual(truncated_words[-1], "word39999")

    def test_word_truncation_small_text(self):
        """Verify that text <= 40000 words is left unchanged."""
        small_text = "this is a small test document"
        words = small_text.split(None, 40001)
        self.assertFalse(len(words) > 40000)
        self.assertEqual(small_text, " ".join(words))

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="sample text chunk content")
    def test_batching_and_flush(self, mock_file, mock_listdir, mock_exists):
        """Verify that documents are batched and flushed correctly to chromadb."""
        mock_exists.return_value = True
        mock_listdir.return_value = [f"doc_{i}.txt" for i in range(25)]

        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        indexer_module.chromadb.PersistentClient.return_value = mock_client

        indexer_module.local_chroma_rag_inject()

        # With 25 files and BATCH_SIZE = 20, collection.add should be called twice (once for 20, once for 5)
        self.assertEqual(mock_collection.add.call_count, 2)

        first_call = mock_collection.add.call_args_list[0][1]
        second_call = mock_collection.add.call_args_list[1][1]

        self.assertEqual(len(first_call["documents"]), 20)
        self.assertEqual(len(second_call["documents"]), 5)

if __name__ == "__main__":
    unittest.main()
