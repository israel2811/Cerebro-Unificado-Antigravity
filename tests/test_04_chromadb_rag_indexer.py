import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import tempfile
import importlib.util

class TestChromaDBRAGIndexer(unittest.TestCase):

    def test_bounded_word_split_small_text(self):
        text = "word " * 100
        words = text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        result = " ".join(words[:40000]) if len(words) > 40000 else text
        self.assertEqual(result, text)

    def test_bounded_word_split_large_text(self):
        # 50,000 words
        words_list = [f"w{i}" for i in range(50000)]
        large_text = " ".join(words_list)

        words = large_text.split(None, 40001)
        self.assertEqual(len(words), 40002) # 40001 splits -> 40002 elements
        self.assertGreater(len(words), 40000)

        truncated = " ".join(words[:40000])
        expected = " ".join(words_list[:40000])
        self.assertEqual(truncated, expected)

    def test_indexer_batching_and_flushing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create 25 sample chunk files
            for i in range(1, 26):
                file_path = os.path.join(tmp_dir, f"chunk_{i:02d}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Sample content for chunk {i}")

            mock_chroma_client = MagicMock()
            mock_collection = MagicMock()
            mock_chroma_client.get_or_create_collection.return_value = mock_collection

            # Mock chromadb in sys.modules
            mock_chromadb = MagicMock()
            mock_chromadb.PersistentClient.return_value = mock_chroma_client
            mock_utils = MagicMock()
            mock_ef = MagicMock()
            mock_utils.embedding_functions = mock_ef
            mock_chromadb.utils = mock_utils

            mock_modules = {
                "chromadb": mock_chromadb,
                "chromadb.utils": mock_utils,
                "chromadb.utils.embedding_functions": mock_ef,
            }

            with patch.dict(sys.modules, mock_modules):
                spec = importlib.util.spec_from_file_location(
                    "indexer",
                    os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
                )
                indexer_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(indexer_module)

                # Override CLEAN_CHUNKS_DIR after exec_module
                indexer_module.CLEAN_CHUNKS_DIR = tmp_dir

                indexer_module.local_chroma_rag_inject()

                # Batch size is 20, so 25 items should result in 2 calls to collection.add
                self.assertEqual(mock_collection.add.call_count, 2)

                # First call batch of 20 items
                first_call_args = mock_collection.add.call_args_list[0][1]
                self.assertEqual(len(first_call_args["documents"]), 20)
                self.assertEqual(len(first_call_args["ids"]), 20)

                # Second call remaining 5 items
                second_call_args = mock_collection.add.call_args_list[1][1]
                self.assertEqual(len(second_call_args["documents"]), 5)
                self.assertEqual(len(second_call_args["ids"]), 5)

if __name__ == "__main__":
    unittest.main()
