import unittest
import os

class TestIndexerOptimization(unittest.TestCase):
    def test_word_truncation_under_limit(self):
        content = "word " * 100
        words = content.split(None, 40000)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = content
        self.assertEqual(result, content)
        self.assertEqual(len(words), 100)

    def test_word_truncation_exact_limit(self):
        words_list = [f"w{i}" for i in range(40000)]
        content = " ".join(words_list)
        words = content.split(None, 40000)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = content
        self.assertEqual(result, content)
        self.assertEqual(len(words), 40000)

    def test_word_truncation_over_limit(self):
        words_list = [f"w{i}" for i in range(50000)]
        content = " ".join(words_list)
        words = content.split(None, 40000)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = content
        expected = " ".join(words_list[:40000])
        self.assertEqual(result, expected)
        self.assertEqual(len(words), 40001)

    def test_deterministic_file_sorting(self):
        files = ["chunk_10.txt", "chunk_1.txt", "chunk_2.txt"]
        sorted_files = sorted(files)
        self.assertEqual(sorted_files, ["chunk_1.txt", "chunk_10.txt", "chunk_2.txt"])

if __name__ == "__main__":
    unittest.main()
