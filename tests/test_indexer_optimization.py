import unittest

class TestIndexerOptimization(unittest.TestCase):
    def test_word_truncation_under_limit(self):
        text = "word " * 100
        words = text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        self.assertEqual(len(words), 100)
        result = " ".join(words[:40000])
        self.assertEqual(result, text.strip())

    def test_word_truncation_exact_limit(self):
        words_expected = [f"w{i}" for i in range(40000)]
        text = " ".join(words_expected)
        words = text.split(None, 40001)
        self.assertEqual(len(words), 40000)
        result = " ".join(words[:40000])
        self.assertEqual(result, text)

    def test_word_truncation_over_limit(self):
        words_input = [f"w{i}" for i in range(50000)]
        text = " ".join(words_input)

        # Original logic simulation
        orig_split = text.split()
        if len(orig_split) > 40000:
            orig_result = " ".join(orig_split[:40000])
        else:
            orig_result = text

        # Optimized logic simulation
        opt_split = text.split(None, 40001)
        if len(opt_split) > 40000:
            opt_result = " ".join(opt_split[:40000])
        else:
            opt_result = text

        self.assertEqual(opt_result, orig_result)
        self.assertEqual(len(opt_result.split()), 40000)

if __name__ == "__main__":
    unittest.main()
