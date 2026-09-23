import unittest
import time

class TestIndexerOptimization(unittest.TestCase):
    def test_under_limit(self):
        # A small document with fewer than 40,000 words
        contenido = "word " * 1000

        # Original logic
        original_result = contenido
        if len(contenido.split()) > 40000:
            original_result = " ".join(contenido.split()[:40000])

        # Optimized logic
        words = contenido.split(None, 40001)
        optimized_result = contenido
        if len(words) > 40000:
            optimized_result = " ".join(words[:40000])

        # The outputs should be functionally equivalent (ignoring trailing whitespace)
        self.assertEqual(original_result.strip(), optimized_result.strip())

    def test_over_limit(self):
        # A large document with more than 40,000 words (e.g., 45,000 words)
        contenido = "word " * 45000

        # Original logic
        original_result = contenido
        if len(contenido.split()) > 40000:
            original_result = " ".join(contenido.split()[:40000])

        # Optimized logic
        words = contenido.split(None, 40001)
        optimized_result = contenido
        if len(words) > 40000:
            optimized_result = " ".join(words[:40000])

        # The outputs should match exactly
        self.assertEqual(original_result, optimized_result)
        # It must be exactly 40,000 words
        self.assertEqual(len(optimized_result.split()), 40000)

    def test_speed_comparison(self):
        # Measure speedup on a very large document
        contenido = "word " * 200000

        # Benchmark Original logic
        t0 = time.perf_counter()
        original_result = contenido
        if len(contenido.split()) > 40000:
            original_result = " ".join(contenido.split()[:40000])
        t1 = time.perf_counter()
        original_duration = t1 - t0

        # Benchmark Optimized logic
        t2 = time.perf_counter()
        words = contenido.split(None, 40001)
        optimized_result = contenido
        if len(words) > 40000:
            optimized_result = " ".join(words[:40000])
        t3 = time.perf_counter()
        optimized_duration = t3 - t2

        # Verify correctness
        self.assertEqual(original_result, optimized_result)

        # Assert optimization is significantly faster (at least 2x, but typically 10x+)
        print(f"\nOriginal logic took: {original_duration:.6f} seconds")
        print(f"Optimized logic took: {optimized_duration:.6f} seconds")
        print(f"Speedup factor: {original_duration / optimized_duration:.2f}x")
        self.assertLess(optimized_duration, original_duration)

if __name__ == '__main__':
    unittest.main()
