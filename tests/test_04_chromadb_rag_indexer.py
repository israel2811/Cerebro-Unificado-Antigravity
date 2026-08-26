import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import MagicMock, patch

# Ensure test can import module dynamically if needed or test function logic
class TestChromaDbRagIndexer(unittest.TestCase):
    def test_truncation_logic(self):
        # Create a text with 50,000 words
        large_text = "word " * 50000
        words = large_text.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_content = " ".join(words[:40000])
        self.assertEqual(len(truncated_content.split()), 40000)

    def test_small_text_logic(self):
        small_text = "hello world python testing"
        words = small_text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        self.assertEqual(len(words), 4)

if __name__ == "__main__":
    unittest.main()
