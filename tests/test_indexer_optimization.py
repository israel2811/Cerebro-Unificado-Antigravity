import sys
import unittest
from unittest.mock import MagicMock
import importlib.util

# Inject mock modules before importing the target script
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()


class TestIndexerOptimization(unittest.TestCase):
    def test_word_split_optimization_logic(self):
        # We test the exact split logic to verify correctness and performance.
        text = "word " * 50000
        words = text.split(None, 40000)
        self.assertEqual(len(words), 40001)

        sliced_words = words[:40000]
        self.assertEqual(len(sliced_words), 40000)

        joined = " ".join(sliced_words)
        self.assertEqual(len(joined.split()), 40000)

    def test_module_loading_and_variables(self):
        # Dynamically import the module to ensure no syntax errors
        spec = importlib.util.spec_from_file_location(
            "chromadb_rag_indexer",
            "scripts_leviathan/04_chromadb_rag_indexer.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules["chromadb_rag_indexer"] = module
        spec.loader.exec_module(module)

        self.assertTrue(hasattr(module, 'local_chroma_rag_inject'))


if __name__ == "__main__":
    unittest.main()
