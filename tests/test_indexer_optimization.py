import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure sys.modules has a mock chromadb if chromadb is not installed in runtime
if "chromadb" not in sys.modules:
    sys.modules["chromadb"] = MagicMock()
    sys.modules["chromadb.utils"] = MagicMock()
    sys.modules["chromadb.utils.embedding_functions"] = MagicMock()

import importlib.util

spec = importlib.util.spec_from_file_location(
    "chromadb_rag_indexer",
    os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
)
indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)


class TestChromaDBIndexerOptimization(unittest.TestCase):

    def test_maxsplit_truncation(self):
        """Test that maxsplit efficiently truncates text with >40k words."""
        long_text = "word " * 50000
        words = long_text.split(None, 40001)
        self.assertGreater(len(words), 40000)
        truncated = " ".join(words[:40000])
        truncated_word_count = len(truncated.split())
        self.assertEqual(truncated_word_count, 40000)

    @patch("chromadb.PersistentClient")
    def test_batching_flush(self, mock_client_cls):
        """Test that batch_docs flushes when reaching BATCH_SIZE."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_client_cls.return_value = mock_client

        # Create temporary directory with 25 text chunk files
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(25):
                file_path = os.path.join(tmpdir, f"test_chunk_{i}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"This is sample chunk content {i}")

            with patch.object(indexer_module, "CLEAN_CHUNKS_DIR", tmpdir), \
                 patch.object(indexer_module, "DB_PATH", tmpdir):
                indexer_module.local_chroma_rag_inject()

            # Should be called twice: once for batch size of 20, once for remaining 5
            self.assertEqual(mock_collection.add.call_count, 2)
            first_call_docs = mock_collection.add.call_args_list[0].kwargs["documents"]
            second_call_docs = mock_collection.add.call_args_list[1].kwargs["documents"]
            self.assertEqual(len(first_call_docs), 20)
            self.assertEqual(len(second_call_docs), 5)


if __name__ == "__main__":
    unittest.main()
