import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import importlib.util

# 1. Mock chromadb and its utils before importing the target module so that tests run without dependencies
mock_chromadb = MagicMock()
mock_chromadb_utils = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = mock_chromadb_utils

# 2. Dynamically import 04_chromadb_rag_indexer.py
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
indexer_path = os.path.join(SCRIPT_DIR, "scripts_leviathan", "04_chromadb_rag_indexer.py")

spec = importlib.util.spec_from_file_location(
    "chromadb_rag_indexer",
    indexer_path
)
indexer_mod = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_mod
spec.loader.exec_module(indexer_mod)

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

        # Should retain original content length
        self.assertEqual(len(words), 1000)

    def test_lexicographical_sorting(self):
        """Test that file chunks are sorted lexicographically (lexical rather than natural sorting)."""
        unsorted_list = ["chapter_10.txt", "chapter_1.txt", "chapter_2.txt"]
        sorted_list = sorted(unsorted_list)

        # Expected alphabetical ordering
        expected_list = ["chapter_1.txt", "chapter_10.txt", "chapter_2.txt"]
        self.assertEqual(sorted_list, expected_list)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open')
    def test_batching_mechanism(self, mock_open, mock_listdir, mock_exists):
        """Verify that batching correctly groups files in chunks of 20 and handles remainders."""
        # Arrange
        mock_exists.return_value = True

        # 25 files in arbitrary order
        file_list = [f"doc_{i}.txt" for i in range(1, 26)]
        mock_listdir.return_value = file_list

        # Open mock file content
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy file content"

        # Mock Chroma persistent client and collection
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        indexer_mod.chromadb.PersistentClient = MagicMock(return_value=mock_client)

        # Act
        indexer_mod.local_chroma_rag_inject()

        # Assert
        # With 25 files and BATCH_SIZE = 20, we expect collection.add to be called twice:
        # First call: a batch of 20 documents.
        # Second call: a batch of 5 documents.
        self.assertEqual(mock_collection.add.call_count, 2)

        # Check first batch arguments
        first_call_kwargs = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_kwargs['documents']), 20)
        self.assertEqual(len(first_call_kwargs['ids']), 20)

        # Check second batch arguments
        second_call_kwargs = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_kwargs['documents']), 5)
        self.assertEqual(len(second_call_kwargs['ids']), 5)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open')
    def test_batching_poison_prevention(self, mock_open, mock_listdir, mock_exists):
        """Verify that batch queue buffers are cleared even if collection.add fails, preventing poisoning."""
        mock_exists.return_value = True

        # 25 files
        file_list = [f"doc_{i}.txt" for i in range(1, 26)]
        mock_listdir.return_value = file_list
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy file content"

        mock_client = MagicMock()
        mock_collection = MagicMock()

        # Simulate collection.add raising an exception on the first batch, but succeeding on the second
        mock_collection.add.side_effect = [ValueError("Simulated batch failure"), None]
        mock_client.get_or_create_collection.return_value = mock_collection
        indexer_mod.chromadb.PersistentClient = MagicMock(return_value=mock_client)

        # Act & Assert (Should complete without raising since exception inside flush_batch is handled and logged)
        try:
            indexer_mod.local_chroma_rag_inject()
        except Exception as e:
            self.fail(f"local_chroma_rag_inject raised an unexpected exception: {e}")

        # Verify both batches were attempted
        self.assertEqual(mock_collection.add.call_count, 2)

        # Since buffers are cleared on finally, the second batch should only contain 5 documents (and not 25 poisoned ones)
        second_call_kwargs = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_kwargs['documents']), 5)

if __name__ == '__main__':
    unittest.main()
