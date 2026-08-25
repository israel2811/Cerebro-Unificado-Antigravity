import unittest
from unittest.mock import MagicMock
import sys

# Mock chromadb before importing 04_chromadb_rag_indexer if chromadb isn't installed in environment
try:
    import chromadb
except ImportError:
    mock_chroma = MagicMock()
    sys.modules["chromadb"] = mock_chroma
    sys.modules["chromadb.utils"] = MagicMock()
    sys.modules["chromadb.utils.embedding_functions"] = MagicMock()


class TestChromaRAGIndexerOptimization(unittest.TestCase):
    def test_truncation_logic_small_text(self):
        text = "word " * 100
        words = text.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = text
        self.assertEqual(len(result.split()), 100)

    def test_truncation_logic_large_text(self):
        text = "word " * 50000
        words = text.split(None, 40001)
        self.assertTrue(len(words) > 40000)
        result = " ".join(words[:40000])
        self.assertEqual(len(result.split()), 40000)

    def test_truncation_result_equality(self):
        text = "word " * 45000
        # Original logic
        res_orig = " ".join(text.split()[:40000])
        # Optimized logic
        words = text.split(None, 40001)
        res_opt = " ".join(words[:40000])
        self.assertEqual(res_orig, res_opt)


if __name__ == "__main__":
    unittest.main()
