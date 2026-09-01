import unittest

class TestChromaDBIndexerOptimization(unittest.TestCase):
    def test_truncation_logic_over_limit(self):
        # Create dummy text with > 40000 words
        words_input = ["word"] * 45000
        content = " ".join(words_input)

        # Optimized maxsplit split logic
        words = content.split(None, 40001)
        if len(words) > 40000:
            truncated = " ".join(words[:40000])
        else:
            truncated = content

        self.assertEqual(len(truncated.split()), 40000)

    def test_truncation_logic_under_limit(self):
        # Create dummy text with <= 40000 words
        words_input = ["word"] * 100
        content = " ".join(words_input)

        # Optimized maxsplit split logic
        words = content.split(None, 40001)
        if len(words) > 40000:
            truncated = " ".join(words[:40000])
        else:
            truncated = content

        self.assertEqual(truncated, content)
        self.assertEqual(len(truncated.split()), 100)

if __name__ == '__main__':
    unittest.main()
