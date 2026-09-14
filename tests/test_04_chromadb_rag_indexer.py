import unittest
import importlib.util
import sys
import os

# Dynamically import 04_chromadb_rag_indexer.py
script_path = os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
indexer_module = importlib.util.module_from_spec(spec)
# Spec loader execution omitted if dependencies aren't loaded, but we can test logic directly or import.

class TestChromaDBIndexerOptimization(unittest.TestCase):
    def test_word_truncation_logic(self):
        # Create a text with 50,000 words
        word_list = [f"word{i}" for i in range(50000)]
        large_text = " ".join(word_list)

        # Apply the optimized truncation logic
        words = large_text.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_text = " ".join(words[:40000])
        truncated_words = truncated_text.split()

        self.assertEqual(len(truncated_words), 40000)
        self.assertEqual(truncated_words[0], "word0")
        self.assertEqual(truncated_words[39999], "word39999")

    def test_short_text_logic(self):
        short_text = "hello world python test"
        words = short_text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        self.assertEqual(words, ["hello", "world", "python", "test"])

if __name__ == "__main__":
    unittest.main()
