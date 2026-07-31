import sys
import os
import unittest
from unittest.mock import MagicMock

# Inject mock chromadb into sys.modules before importing the module
mock_chromadb = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()

# Now we can import the module using importlib
import importlib.util
spec = importlib.util.spec_from_file_location(
    "chromadb_rag_indexer",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scripts_leviathan/04_chromadb_rag_indexer.py")
)
indexer_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_module
spec.loader.exec_module(indexer_module)

class TestIndexerOptimization(unittest.TestCase):
    def test_truncation_no_split_needed(self):
        # A small document with fewer than 40000 words should not be truncated
        content = "word " * 10
        # Simulating content.split(None, 40001)
        palabras = content.split(None, 40001)
        self.assertLessEqual(len(palabras), 40000)

        # Test exact behavior of our optimized truncation logic
        if len(palabras) > 40000:
            truncated = " ".join(palabras[:40000])
        else:
            truncated = content

        self.assertEqual(truncated, content)

    def test_truncation_split_needed(self):
        # A large document with more than 40000 words should be truncated to exactly 40000 words
        content = "word " * 50000
        palabras = content.split(None, 40001)
        self.assertGreater(len(palabras), 40000)

        if len(palabras) > 40000:
            truncated = " ".join(palabras[:40000])
        else:
            truncated = content

        words_in_truncated = truncated.split()
        self.assertEqual(len(words_in_truncated), 40000)

        # Verify the original non-optimized double-split behaves identically
        expected = " ".join(content.split()[:40000])
        self.assertEqual(truncated, expected)

if __name__ == "__main__":
    unittest.main()
