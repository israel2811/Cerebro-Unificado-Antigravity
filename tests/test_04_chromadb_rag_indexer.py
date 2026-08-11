import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import importlib.util

# 1. Mock chromadb and its utils before importing the target module
mock_chromadb = MagicMock()
mock_chromadb_utils = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = mock_chromadb_utils

# 2. Dynamically import 04_chromadb_rag_indexer.py
spec = importlib.util.spec_from_file_location(
    "chromadb_rag_indexer",
    "scripts_leviathan/04_chromadb_rag_indexer.py"
)
indexer_mod = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_mod
spec.loader.exec_module(indexer_mod)

class TestChromaDBRagIndexer(unittest.TestCase):
    def test_word_count_truncation(self):
        # We want to verify the truncation logic directly or by calling local_chroma_rag_inject with mocked filesystem.
        # But wait, local_chroma_rag_inject uses os.listdir and open() on files.

        large_text = "word " * 50000

        # Mocking os.path.exists and os.listdir
        with patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=['chunk_1.txt']), \
             patch('builtins.open', unittest.mock.mock_open(read_data=large_text)):

             # Mock Chroma client and get_or_create_collection
             mock_client = MagicMock()
             mock_collection = MagicMock()
             mock_client.get_or_create_collection.return_value = mock_collection
             indexer_mod.chromadb.PersistentClient = MagicMock(return_value=mock_client)

             indexer_mod.local_chroma_rag_inject()

             # Verify that collection.add was called
             mock_collection.add.assert_called_once()

             # Extract arguments from mock call
             kwargs = mock_collection.add.call_args[1]
             documents = kwargs.get('documents', [])
             self.assertEqual(len(documents), 1)
             doc_word_count = len(documents[0].split())
             self.assertEqual(doc_word_count, 40000)

    def test_alphabetical_sorting(self):
        # Verify that os.listdir results are sorted alphabetically (lexicographical sorting).
        # We want to make sure file order processed is: chapter_1.txt, chapter_10.txt, chapter_2.txt
        # instead of arbitrary/original mock order.

        unsorted_files = ['chapter_2.txt', 'chapter_10.txt', 'chapter_1.txt']

        with patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=unsorted_files), \
             patch('builtins.open', unittest.mock.mock_open(read_data="some content")):

             mock_client = MagicMock()
             mock_collection = MagicMock()
             mock_client.get_or_create_collection.return_value = mock_collection
             indexer_mod.chromadb.PersistentClient = MagicMock(return_value=mock_client)

             indexer_mod.local_chroma_rag_inject()

             # Capture the documents and ids added
             # In alphabetical order, chapter_1.txt is first, then chapter_10.txt, then chapter_2.txt
             # We can verify call order of collection.add
             calls = mock_collection.add.call_args_list
             self.assertEqual(len(calls), 3)

             added_ids = [call[1]['ids'][0] for call in calls]

             # Deterministic IDs should be chunk_1_chapter_1.txt, chunk_2_chapter_10.txt, chunk_3_chapter_2.txt
             # (since 'i' is the loop index 1..N after sorting)
             expected_ids = ['chunk_1_chapter_1.txt', 'chunk_2_chapter_10.txt', 'chunk_3_chapter_2.txt']
             self.assertEqual(added_ids, expected_ids)

if __name__ == '__main__':
    unittest.main()
