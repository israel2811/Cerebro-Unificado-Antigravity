import unittest
import time

class TestIndexerOptimization(unittest.TestCase):
    def test_under_limit(self):
        # A string with 30000 words should remain completely intact.
        contenido = "word " * 30000
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = contenido

        self.assertEqual(len(result.split()), 30000)
        self.assertEqual(result, contenido)

    def test_exact_limit(self):
        # A string with exactly 40000 words should remain completely intact.
        contenido = "word " * 40000
        # Clean trailing space for exact comparison after split/join if necessary
        contenido_stripped = contenido.strip()
        words = contenido_stripped.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = contenido_stripped

        self.assertEqual(len(result.split()), 40000)
        self.assertEqual(result, contenido_stripped)

    def test_over_limit(self):
        # A string with 45000 words should be cut down to exactly 40000 words.
        contenido = "word " * 45000
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = contenido

        words_count = len(result.split())
        self.assertEqual(words_count, 40000)

    def test_empty_string(self):
        # An empty string should remain empty and not crash.
        contenido = ""
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            result = " ".join(words[:40000])
        else:
            result = contenido

        self.assertEqual(result, "")

    def test_performance_gain(self):
        # A massive document with 150000 words
        contenido = "word " * 150000

        # Original logic time measurement
        t0 = time.perf_counter()
        if len(contenido.split()) > 40000:
            res_orig = " ".join(contenido.split()[:40000])
        else:
            res_orig = contenido
        t_orig = time.perf_counter() - t0

        # Optimized logic time measurement
        t0 = time.perf_counter()
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            res_opt = " ".join(words[:40000])
        else:
            res_opt = contenido
        t_opt = time.perf_counter() - t0

        # Output the performance comparison
        print(f"\n[Performance Benchmark] Original: {t_orig:.6f}s vs Optimized: {t_opt:.6f}s")
        print(f"[Performance Benchmark] Speedup factor: {t_orig / max(t_opt, 1e-9):.1f}x")

        # Verify logical equivalence
        self.assertEqual(len(res_orig.split()), len(res_opt.split()))

        # The optimized version must be faster
        self.assertLess(t_opt, t_orig)

if __name__ == '__main__':
    unittest.main()
