import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Inject mock chromadb into sys.modules to allow importing module under test
mock_chromadb = MagicMock()
mock_embedding_functions = MagicMock()
mock_chromadb.utils.embedding_functions = mock_embedding_functions
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = mock_chromadb.utils
sys.modules['chromadb.utils.embedding_functions'] = mock_embedding_functions

import importlib.util

indexer_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts_leviathan",
    "04_chromadb_rag_indexer.py"
)
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", indexer_path)
indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer)


class TestChromaDbIndexerOptimization(unittest.TestCase):

    def test_maxsplit_word_truncation_small_text(self):
        text = "word " * 100
        words = text.split(None, 40000)
        self.assertEqual(len(words), 100)

    def test_maxsplit_word_truncation_large_text(self):
        text = "word " * 50000
        words = text.split(None, 40000)
        self.assertEqual(len(words), 40001)
        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    def test_batch_injection_grouping(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            chunks_dir = os.path.join(tmp_dir, "clean_chunks")
            os.makedirs(chunks_dir, exist_ok=True)

            # Create 25 chunk files to test batching (batch of 20 + final batch of 5)
            for i in range(1, 26):
                file_path = os.path.join(chunks_dir, f"chunk_{i:02d}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Sample content for chunk {i}")

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client

            with patch.object(indexer, "CLEAN_CHUNKS_DIR", chunks_dir), \
                 patch.object(indexer, "DB_PATH", os.path.join(tmp_dir, "nexus_vector_db")):
                indexer.local_chroma_rag_inject()

            # Expect 2 batch calls: 1 call with 20 docs, 1 call with 5 docs
            self.assertEqual(mock_collection.add.call_count, 2)

            first_call_kwargs = mock_collection.add.call_args_list[0][1]
            second_call_kwargs = mock_collection.add.call_args_list[1][1]

            self.assertEqual(len(first_call_kwargs["documents"]), 20)
            self.assertEqual(len(second_call_kwargs["documents"]), 5)


if __name__ == "__main__":
    unittest.main()
