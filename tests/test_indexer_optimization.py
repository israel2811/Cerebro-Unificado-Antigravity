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
        self.assertEqual(truncate_words_legacy(text, 40000), truncate_words_optimized(text, 40000))

    def test_truncation_over_limit(self):
        text = "word " * 50000
        legacy_result = truncate_words_legacy(text, 40000)
        optimized_result = truncate_words_optimized(text, 40000)
        self.assertEqual(legacy_result, optimized_result)
        self.assertEqual(len(optimized_result.split()), 40000)

    def test_truncation_exact_limit(self):
        text = "word " * 40000
        self.assertEqual(truncate_words_legacy(text, 40000), truncate_words_optimized(text, 40000))

if __name__ == "__main__":
    unittest.main()
