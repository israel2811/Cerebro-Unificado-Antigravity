import unittest
import sys
import os
import time
import importlib.util

# Ensure the scripts_leviathan directory can be imported
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan")
sys.path.append(scripts_dir)

# Load the numeric-prefixed module dynamically
module_path = os.path.join(scripts_dir, "02_docs_prep_injector.py")
spec = importlib.util.spec_from_file_location("docs_prep_injector", module_path)
docs_prep = importlib.util.module_from_spec(spec)
sys.modules["docs_prep_injector"] = docs_prep
spec.loader.exec_module(docs_prep)

class TestPrepInjector(unittest.TestCase):
    def test_clean_html_noise_basic(self):
        raw = "Hello <b>world</b> {this is JSON} test"
        cleaned = docs_prep.clean_html_noise(raw)
        self.assertIn("Hello", cleaned)
        self.assertIn("world", cleaned)
        self.assertNotIn("JSON", cleaned)

    def test_clean_html_noise_no_brackets(self):
        raw = "Hello world test"
        cleaned = docs_prep.clean_html_noise(raw)
        self.assertEqual("Hello world test", cleaned.strip())

    def test_clean_html_noise_unpaired_brackets_backtracking(self):
        # Unpaired brackets should not cause catastrophic backtracking/hangs
        raw = "Hello {unpaired brackets here that has no ending brace."

        t0 = time.perf_counter()
        cleaned = docs_prep.clean_html_noise(raw)
        duration = time.perf_counter() - t0

        # Should be extremely fast, way under 0.1s
        self.assertLess(duration, 0.1)
        self.assertIn("Hello {unpaired brackets here", cleaned)

    def test_clean_html_noise_multiple_brackets(self):
        raw = "Hello {first} middle {second} end"
        cleaned = docs_prep.clean_html_noise(raw)
        cleaned_compact = " ".join(cleaned.split())
        self.assertEqual("Hello middle end", cleaned_compact)

if __name__ == "__main__":
    unittest.main()
