import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Mock chromadb modules before importing target script
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()

import importlib.util
spec = importlib.util.spec_from_file_location('chroma_indexer', 'scripts_leviathan/04_chromadb_rag_indexer.py')
chroma_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chroma_indexer)

class TestChromaRAGIndexerOptimization(unittest.TestCase):
    def test_word_truncation_optimization(self):
        """Verify that strings with >40,000 words are correctly truncated to 40,000 words."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            chunk_file = os.path.join(tmp_dir, "test_large_chunk.txt")
            large_text = " ".join(["word" + str(i) for i in range(50000)])
            with open(chunk_file, "w", encoding="utf-8") as f:
                f.write(large_text)

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection

            with patch.object(chroma_indexer.chromadb, "PersistentClient", return_value=mock_client), \
                 patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", tmp_dir):
                chroma_indexer.local_chroma_rag_inject()

            mock_collection.add.assert_called_once()
            args, kwargs = mock_collection.add.call_args
            added_docs = kwargs.get("documents", args[0] if args else [])
            doc_content = added_docs[0]
            word_count = len(doc_content.split())
            self.assertEqual(word_count, 40000)

    def test_small_file_no_truncation(self):
        """Verify that strings with <40,000 words are not truncated."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            chunk_file = os.path.join(tmp_dir, "test_small_chunk.txt")
            small_text = "hello world test python"
            with open(chunk_file, "w", encoding="utf-8") as f:
                f.write(small_text)

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection

            with patch.object(chroma_indexer.chromadb, "PersistentClient", return_value=mock_client), \
                 patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", tmp_dir):
                chroma_indexer.local_chroma_rag_inject()

            mock_collection.add.assert_called_once()
            args, kwargs = mock_collection.add.call_args
            added_docs = kwargs.get("documents", args[0] if args else [])
            self.assertEqual(added_docs[0], small_text)

if __name__ == "__main__":
    unittest.main()
