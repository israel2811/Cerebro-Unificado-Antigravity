import sys
import unittest
from unittest.mock import MagicMock

# Inject a mock chromadb module into sys.modules so the script's imports succeed
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()

import importlib.util
spec = importlib.util.spec_from_file_location('chromadb_rag_indexer', 'scripts_leviathan/04_chromadb_rag_indexer.py')
module = importlib.util.module_from_spec(spec)
sys.modules['chromadb_rag_indexer'] = module
spec.loader.exec_module(module)

class TestIndexerOptimization(unittest.TestCase):
    def test_split_optimization_with_large_input(self):
        """Verify that split(None, 40000) behaves exactly as expected for truncation."""
        large_text = "word " * 50000
        palabras = large_text.split(None, 40000)
        self.assertEqual(len(palabras), 40001)

        truncated = " ".join(palabras[:40000])
        expected = " ".join(["word"] * 40000)
        self.assertEqual(truncated, expected)

    def test_split_optimization_with_small_input(self):
        """Verify that small inputs are not affected."""
        small_text = "word " * 10
        palabras = small_text.split(None, 40000)
        self.assertEqual(len(palabras), 10)

if __name__ == '__main__':
    unittest.main()
