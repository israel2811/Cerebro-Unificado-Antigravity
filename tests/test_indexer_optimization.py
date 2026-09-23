import unittest

class TestIndexerOptimization(unittest.TestCase):
    def test_truncation_under_limit(self):
        content = "hello world python test code"
        words = content.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = content
        self.assertEqual(result, content)

    def test_truncation_exact_limit(self):
        words_40k = ["word"] * 40000
        content = " ".join(words_40k)
        words = content.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = content
        self.assertEqual(result, content)

    def test_truncation_over_limit(self):
        words_50k = [f"w{i}" for i in range(50000)]
        content = " ".join(words_50k)

        # Original logic
        orig_split = content.split()
        if len(orig_split) > 40000:
            expected = " ".join(orig_split[:40000])
        else:
            expected = content

        # Optimized logic
        words = content.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = content

        self.assertEqual(result, expected)
        self.assertEqual(len(result.split()), 40000)

if __name__ == "__main__":
    unittest.main()
