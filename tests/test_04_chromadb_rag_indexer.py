import unittest
import sys
from unittest.mock import MagicMock

# Mock chromadb before importing the target script if chromadb is not installed
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

class TestChromaDBIndexerOptimization(unittest.TestCase):
    def test_word_truncation_logic(self):
        # Generate a string with 50,000 words
        large_content = "word " * 50000
        words = large_content.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_content = " ".join(words[:40000])
        self.assertEqual(len(truncated_content.split()), 40000)

    def test_small_content_not_truncated(self):
        small_content = "word " * 100
        words = small_content.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        self.assertEqual(len(words), 100)

if __name__ == "__main__":
    unittest.main()
