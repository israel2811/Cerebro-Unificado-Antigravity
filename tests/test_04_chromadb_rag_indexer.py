import unittest

class TestIndexerOptimization(unittest.TestCase):
    def test_maxsplit_truncation_under_limit(self):
        # 100 words text
        text = "word " * 100
        words = text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        self.assertEqual(len(words), 100)

    def test_maxsplit_truncation_over_limit(self):
        # 50,000 words text
        text = "word " * 50000
        words = text.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_content = " ".join(words[:40000])
        truncated_words = truncated_content.split()
        self.assertEqual(len(truncated_words), 40000)

    def test_maxsplit_equivalence(self):
        # Test that old method and new method produce identical output
        text = "hello world " * 5000
        # Old method
        if len(text.split()) > 40000:
            res_old = " ".join(text.split()[:40000])
        else:
            res_old = text

        # New method
        words = text.split(None, 40001)
        if len(words) > 40000:
            res_new = " ".join(words[:40000])
        else:
            res_new = text

        self.assertEqual(res_old, res_new)

if __name__ == "__main__":
    unittest.main()
