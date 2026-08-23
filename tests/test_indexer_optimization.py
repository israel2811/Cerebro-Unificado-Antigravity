import unittest

def truncate_words_legacy(contenido: str, max_words: int = 40000) -> str:
    if len(contenido.split()) > max_words:
        return " ".join(contenido.split()[:max_words])
    return contenido

def truncate_words_optimized(contenido: str, max_words: int = 40000) -> str:
    words = contenido.split(None, max_words + 1)
    if len(words) > max_words:
        return " ".join(words[:max_words])
    return contenido

class TestIndexerOptimization(unittest.TestCase):
    def test_truncation_under_limit(self):
        text = "word " * 100
        self.assertEqual(truncate_words_legacy(text, 1000), truncate_words_optimized(text, 1000))
        self.assertEqual(truncate_words_optimized(text, 1000), text)

    def test_truncation_over_limit(self):
        text = "word1 word2 word3 word4 word5"
        self.assertEqual(truncate_words_legacy(text, 3), "word1 word2 word3")
        self.assertEqual(truncate_words_optimized(text, 3), "word1 word2 word3")
        self.assertEqual(truncate_words_legacy(text, 3), truncate_words_optimized(text, 3))

    def test_truncation_whitespace_handling(self):
        text = "  hello   world   foo   bar   baz  "
        self.assertEqual(truncate_words_legacy(text, 3), truncate_words_optimized(text, 3))

if __name__ == "__main__":
    unittest.main()
