import unittest

def truncate_original(contenido):
    if len(contenido.split()) > 40000:
        return " ".join(contenido.split()[:40000])
    return contenido

def truncate_optimized(contenido):
    words_chunk = contenido.split(None, 40000)
    if len(words_chunk) > 40000:
        return " ".join(words_chunk[:40000])
    return contenido

class TestChromaRAGIndexerOptimization(unittest.TestCase):
    def test_short_text(self):
        text = "word " * 100
        self.assertEqual(truncate_optimized(text), truncate_original(text))

    def test_exact_40000_words(self):
        text = "word " * 40000
        self.assertEqual(len(truncate_optimized(text).split()), 40000)
        self.assertEqual(truncate_optimized(text), truncate_original(text))

    def test_over_40000_words(self):
        text = " ".join([f"word{i}" for i in range(50000)])
        result_opt = truncate_optimized(text)
        result_orig = truncate_original(text)

        self.assertEqual(len(result_opt.split()), 40000)
        self.assertEqual(result_opt, result_orig)

if __name__ == "__main__":
    unittest.main()
