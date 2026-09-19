import unittest

def truncate_text_optimized(contenido, max_words=40000):
    words = contenido.split(None, max_words)
    if len(words) > max_words:
        return " ".join(words[:max_words])
    return contenido

def truncate_text_legacy(contenido, max_words=40000):
    if len(contenido.split()) > max_words:
        return " ".join(contenido.split()[:max_words])
    return contenido

class TestIndexerOptimization(unittest.TestCase):
    def test_small_text_preservation(self):
        text = "Hello world! This is a short test document."
        self.assertEqual(truncate_text_optimized(text), text)
        self.assertEqual(truncate_text_optimized(text), truncate_text_legacy(text))

    def test_exact_limit_text(self):
        words = [f"word{i}" for i in range(40000)]
        text = " ".join(words)
        self.assertEqual(truncate_text_optimized(text), text)
        self.assertEqual(truncate_text_optimized(text), truncate_text_legacy(text))

    def test_over_limit_text_truncation(self):
        words = [f"word{i}" for i in range(50000)]
        text = " ".join(words)
        result = truncate_text_optimized(text)
        result_words = result.split()
        self.assertEqual(len(result_words), 40000)
        self.assertEqual(result_words[0], "word0")
        self.assertEqual(result_words[-1], "word39999")
        self.assertEqual(result, truncate_text_legacy(text))

if __name__ == "__main__":
    unittest.main()
