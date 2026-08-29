import unittest
import sys
import os

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestIndexerOptimization(unittest.TestCase):
    def test_original_vs_optimized_small_string(self):
        # A small string with 5 words
        small_string = "this is a small string"

        # Original logic:
        # words_count = len(small_string.split())
        # if words_count > 40000:
        #     res_orig = " ".join(small_string.split()[:40000])
        # else:
        #     res_orig = small_string
        res_orig = small_string

        # Optimized logic:
        palabras_split = small_string.split(None, 40001)
        if len(palabras_split) > 40000:
            res_opt = " ".join(palabras_split[:40000])
        else:
            res_opt = small_string

        self.assertEqual(res_orig, res_opt)
        self.assertEqual(len(res_opt.split()), 5)

    def test_original_vs_optimized_large_string(self):
        # Create a simulated string of 45,000 words
        words = ["word"] * 45000
        large_string = " ".join(words)

        # Original logic
        words_count = len(large_string.split())
        self.assertTrue(words_count > 40000)
        res_orig = " ".join(large_string.split()[:40000])

        # Optimized logic
        palabras_split = large_string.split(None, 40001)
        self.assertTrue(len(palabras_split) > 40000)
        res_opt = " ".join(palabras_split[:40000])

        self.assertEqual(res_orig, res_opt)
        self.assertEqual(len(res_opt.split()), 40000)

    def test_empty_string(self):
        empty_string = ""
        palabras_split = empty_string.split(None, 40001)
        if len(palabras_split) > 40000:
            res_opt = " ".join(palabras_split[:40000])
        else:
            res_opt = empty_string

        self.assertEqual(res_opt, "")
        self.assertEqual(len(palabras_split), 0)

    def test_exact_boundary(self):
        # String with exactly 40,000 words
        words = ["word"] * 40000
        boundary_string = " ".join(words)

        palabras_split = boundary_string.split(None, 40001)
        self.assertEqual(len(palabras_split), 40000)

        if len(palabras_split) > 40000:
            res_opt = " ".join(palabras_split[:40000])
        else:
            res_opt = boundary_string

        self.assertEqual(res_opt, boundary_string)

if __name__ == "__main__":
    unittest.main()
