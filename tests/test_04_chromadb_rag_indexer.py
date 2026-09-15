import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch, call
import importlib.util

# Mock chromadb in sys.modules if not available in the environment
if 'chromadb' not in sys.modules:
    chroma_mock = MagicMock()
    sys.modules['chromadb'] = chroma_mock
    sys.modules['chromadb.utils'] = MagicMock()
    sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

# Dynamically import 04_chromadb_rag_indexer.py
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chroma_indexer", os.path.abspath(SCRIPT_PATH))
chroma_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chroma_indexer)

class TestChromaIndexerOptimization(unittest.TestCase):

    def test_word_truncation_under_limit(self):
        content = "word " * 100
        words = content.split(None, 40001)
        self.assertLessEqual(len(words), 40000)

    def test_word_truncation_over_limit(self):
        content = "word " * 50000
        words = content.split(None, 40001)
        self.assertGreater(len(words), 40000)
        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    def test_local_chroma_rag_inject_batching(self):
        with tempfile.TemporaryDirectory() as tmp_chunks_dir, tempfile.TemporaryDirectory() as tmp_db_dir:
            # Create 25 dummy txt files
            for i in range(1, 26):
                file_path = os.path.join(tmp_chunks_dir, f"chunk_{i:02d}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"This is chunk number {i} with some sample test content.")

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection

            with patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", tmp_chunks_dir), \
                 patch.object(chroma_indexer, "DB_PATH", tmp_db_dir), \
                 patch.object(chroma_indexer.chromadb, "PersistentClient", return_value=mock_client):

                chroma_indexer.local_chroma_rag_inject()

                # Verify collection.add was called twice (batch of 20, then batch of 5)
                self.assertEqual(mock_collection.add.call_count, 2)

                # Check first batch size (20 items)
                first_call_args = mock_collection.add.call_args_list[0][1]
                self.assertEqual(len(first_call_args["documents"]), 20)
                self.assertEqual(len(first_call_args["ids"]), 20)

                # Check second batch size (5 items)
                second_call_args = mock_collection.add.call_args_list[1][1]
                self.assertEqual(len(second_call_args["documents"]), 5)
                self.assertEqual(len(second_call_args["ids"]), 5)

if __name__ == "__main__":
    unittest.main()
