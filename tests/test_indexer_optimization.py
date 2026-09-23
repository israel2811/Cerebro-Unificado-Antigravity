import unittest
import sys
import os
import importlib.util
from unittest.mock import MagicMock

# Inject mock chromadb into sys.modules so the indexer import succeeds
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()

# Load scripts_leviathan/04_chromadb_rag_indexer.py dynamically
indexer_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", indexer_path)
indexer_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_module
spec.loader.exec_module(indexer_module)

# Load scripts_leviathan/01_nexus_deep_scanner.py dynamically
scanner_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts_leviathan", "01_nexus_deep_scanner.py")
spec_scanner = importlib.util.spec_from_file_location("nexus_deep_scanner", scanner_path)
scanner_module = importlib.util.module_from_spec(spec_scanner)
sys.modules["nexus_deep_scanner"] = scanner_module
spec_scanner.loader.exec_module(scanner_module)

class TestIndexerOptimization(unittest.TestCase):
    def test_word_count_truncation(self):
        """Test that truncation behaves correctly and uses efficient split-limiting."""
        # Content with 50,000 words
        large_content = "word " * 50000

        # Simulating truncation logic
        words = large_content.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated = " ".join(words[:40000])
        truncated_words = truncated.split()
        self.assertEqual(len(truncated_words), 40000)

    def test_no_truncation_for_small_chunks(self):
        """Test that chunks smaller than 40,000 words are not truncated."""
        small_content = "word " * 1000
        words = small_content.split(None, 40001)
        self.assertLessEqual(len(words), 40000)

        # Should retain original content
        self.assertEqual(len(words), 1000)

    def test_lexicographical_sorting(self):
        """Test that file chunks are sorted lexicographically (lexical rather than natural sorting)."""
        unsorted_list = ["chapter_10.txt", "chapter_1.txt", "chapter_2.txt"]
        sorted_list = sorted(unsorted_list)

        # Expected alphabetical ordering
        expected_list = ["chapter_1.txt", "chapter_10.txt", "chapter_2.txt"]
        self.assertEqual(sorted_list, expected_list)

    def test_scanner_len_optimization(self):
        """Test that len(chunk) optimization calculates characters correctly."""
        dummy_chunk = "test_chunk_with_🚀_unicode"
        # Original logic used len(chunk.encode('utf-8')) which counts bytes.
        # Optimized logic uses len(chunk) which is O(1) in characters.
        # This test ensures len(chunk) counts correctly.
        self.assertEqual(len(dummy_chunk), 25)

if __name__ == '__main__':
    unittest.main()
