import os
import sys
import unittest
import importlib.util

# Ensure python can find scripts_leviathan
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TestIndexerOptimization(unittest.TestCase):
    def test_split_optimization_small(self):
        # Under 40,000 words, it should return the original string (with normalized spaces)
        original_text = "hello world from jules"
        words = original_text.split(None, 40001)
        self.assertLessEqual(len(words), 40000)
        reconstructed = " ".join(words[:40000])
        self.assertEqual(reconstructed, "hello world from jules")

    def test_split_optimization_large(self):
        # Exactly 50,000 words
        original_words = ["word"] * 50000
        original_text = " ".join(original_words)

        words = original_text.split(None, 40001)
        self.assertGreater(len(words), 40000)

        reconstructed = " ".join(words[:40000])
        reconstructed_words = reconstructed.split()

        self.assertEqual(len(reconstructed_words), 40000)
        self.assertEqual(reconstructed_words, original_words[:40000])

    def test_paths_exist(self):
        # Verify module imports and resolves SCRIPT_DIR correctly
        spec = importlib.util.spec_from_file_location(
            "rag_indexer",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py"))
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertTrue(hasattr(module, "CLEAN_CHUNKS_DIR"))
        self.assertTrue(hasattr(module, "DB_PATH"))

        expected_chunks_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "scripts_leviathan", "clean_chunks"
        ))
        self.assertEqual(os.path.abspath(module.CLEAN_CHUNKS_DIR), expected_chunks_dir)

if __name__ == "__main__":
    unittest.main()
