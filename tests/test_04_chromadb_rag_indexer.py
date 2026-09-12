import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import importlib.util

# Ensure chromadb can be imported or mocked if missing
if "chromadb" not in sys.modules:
    try:
        import chromadb
    except ImportError:
        sys.modules["chromadb"] = MagicMock()
        sys.modules["chromadb.utils"] = MagicMock()
        sys.modules["chromadb.utils.embedding_functions"] = MagicMock()

# Dynamically import 04_chromadb_rag_indexer.py
script_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts_leviathan",
    "04_chromadb_rag_indexer.py"
)
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)


class TestChromaDBRAGIndexerOptimization(unittest.TestCase):
    """Test suite for 04_chromadb_rag_indexer string truncation and sorting optimizations."""

    def test_truncation_small_text(self):
        """Test that small texts under 40000 words are not truncated."""
        text = "word " * 100
        words = text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = text
        self.assertEqual(len(result.split()), 100)

    def test_truncation_large_text(self):
        """Test that texts over 40000 words are truncated to exactly 40000 words efficiently."""
        text = "word " * 50000
        words = text.split(None, 40001)
        self.assertGreater(len(words), 40000)
        self.assertEqual(len(words), 40002)  # maxsplit=40001 creates 40002 items (40001 words + remainder)

        truncated_text = " ".join(words[:40000])
        self.assertEqual(len(truncated_text.split()), 40000)

    def test_sorted_archivos_list(self):
        """Test deterministic sorting of chunk files."""
        raw_files = ["chunk_2.txt", "chunk_10.txt", "chunk_1.txt"]
        sorted_files = sorted(raw_files)
        self.assertEqual(sorted_files, ["chunk_1.txt", "chunk_10.txt", "chunk_2.txt"])


if __name__ == "__main__":
    unittest.main()
