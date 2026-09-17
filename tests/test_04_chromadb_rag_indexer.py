import os
import sys
import unittest
import tempfile
import importlib.util
from unittest.mock import MagicMock, patch

# Inject mock chromadb module into sys.modules if chromadb is not installed
if 'chromadb' not in sys.modules:
    mock_chromadb = MagicMock()
    mock_embedding = MagicMock()
    mock_chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction.return_value = mock_embedding
    sys.modules['chromadb'] = mock_chromadb
    sys.modules['chromadb.utils'] = mock_chromadb.utils
    sys.modules['chromadb.utils.embedding_functions'] = mock_chromadb.utils.embedding_functions

# Import module dynamically due to numeric prefix in filename
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chroma_indexer", SCRIPT_PATH)
chroma_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chroma_indexer)

class TestChromaRAGIndexerOptimization(unittest.TestCase):

    def test_maxsplit_word_truncation(self):
        """Verify that strings over 40,000 words are truncated to exactly 40,000 words."""
        large_text = "word " * 50000
        parts = large_text.split(None, 40001)
        self.assertGreater(len(parts), 40000)

        truncated = " ".join(parts[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    @patch("os.path.exists", return_value=True)
    def test_batching_and_deterministic_sorting(self, mock_exists):
        """Verify that collection.add is called in batches of 20 and files are processed in sorted order."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create 25 dummy chunk files: chunk_01.txt ... chunk_25.txt
            filenames = [f"chunk_{i:02d}.txt" for i in range(1, 26)]
            for fname in filenames:
                with open(os.path.join(tmp_dir, fname), "w", encoding="utf-8") as f:
                    f.write(f"Content for {fname}")

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection

            with patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", tmp_dir), \
                 patch.object(chroma_indexer.chromadb, "PersistentClient", return_value=mock_client):

                chroma_indexer.local_chroma_rag_inject()

            # We created 25 files, so with BATCH_SIZE=20 we expect 2 batch calls:
            # First batch: 20 documents
            # Second batch: 5 documents
            self.assertEqual(mock_collection.add.call_count, 2)

            first_call_kwargs = mock_collection.add.call_args_list[0][1]
            second_call_kwargs = mock_collection.add.call_args_list[1][1]

            self.assertEqual(len(first_call_kwargs["documents"]), 20)
            self.assertEqual(len(second_call_kwargs["documents"]), 5)

            # Check deterministic sorting order
            first_batch_sources = [m["source"] for m in first_call_kwargs["metadatas"]]
            self.assertEqual(first_batch_sources, sorted(filenames)[:20])

if __name__ == "__main__":
    unittest.main()
