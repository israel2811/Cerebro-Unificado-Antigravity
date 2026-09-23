import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import importlib.util

# 1. Mock chromadb and other heavy modules before loading the target module
mock_chromadb = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()

# 2. Dynamic import of the target module with a numeric prefix
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts_leviathan", "04_chromadb_rag_indexer.py")
spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", SCRIPT_PATH)
indexer_module = importlib.util.module_from_spec(spec)
sys.modules["chromadb_rag_indexer"] = indexer_module
spec.loader.exec_module(indexer_module)

class TestChromaDBRagIndexer(unittest.TestCase):
    def setUp(self):
        # Reset mocks
        mock_chromadb.reset_mock()

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open')
    def test_rag_injection_batching_and_splitting(self, mock_file_open, mock_listdir, mock_exists):
        # Configure path existence
        mock_exists.return_value = True

        # We will return 25 text chunks to test batching (size 20)
        chunk_files = [f"chunk_{i:02d}.txt" for i in range(1, 26)]
        # Return them in unsorted order to verify sorting works
        mock_listdir.return_value = list(reversed(chunk_files))

        # Create a large text for chunk 1 (>40000 words)
        large_text = "word " * 50000
        # Create a small text for other chunks
        small_text = "short text"

        # Configure file reading
        # We want to return large_text for chunk_01.txt, and small_text for the rest
        def open_side_effect(filepath, mode="r", *args, **kwargs):
            filename = os.path.basename(filepath)
            content = large_text if filename == "chunk_01.txt" else small_text
            return mock_open(read_data=content)()

        mock_file_open.side_effect = open_side_effect

        # Mock ChromaDB components
        mock_client = MagicMock()
        mock_collection = MagicMock()

        mock_chromadb.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # To prevent list clearing in 'finally' block from wiping mock call arguments,
        # we store copies of added arguments in a list of captured calls.
        captured_add_calls = []
        def capture_add(*args, **kwargs):
            # Capture copies of documents, metadatas, and ids
            captured_add_calls.append({
                'documents': list(kwargs.get('documents', [])),
                'metadatas': list(kwargs.get('metadatas', [])),
                'ids': list(kwargs.get('ids', []))
            })
            return None

        mock_collection.add.side_effect = capture_add

        # Run the injector
        indexer_module.local_chroma_rag_inject()

        # Assertions
        # 1. Sorting verification (files processed alphabetically)
        # 2. Batching verification: 25 files should result in:
        #    - Batch 1: 20 documents
        #    - Batch 2 (Flush): 5 documents
        self.assertEqual(len(captured_add_calls), 2)

        # Check first batch size
        self.assertEqual(len(captured_add_calls[0]['documents']), 20)
        # Check second batch size
        self.assertEqual(len(captured_add_calls[1]['documents']), 5)

        # Verify the large file split/truncation
        # The first alphabetical file is chunk_01.txt, so it should be the first item in the first batch
        first_doc = captured_add_calls[0]['documents'][0]
        first_doc_word_count = len(first_doc.split())
        self.assertEqual(first_doc_word_count, 40000)

        # Check that metadata of the first doc matches chunk_01.txt
        first_meta = captured_add_calls[0]['metadatas'][0]
        self.assertEqual(first_meta['source'], 'chunk_01.txt')

        # Verify other files are in alphabetical order
        for idx, meta in enumerate(captured_add_calls[0]['metadatas']):
            expected_filename = f"chunk_{idx+1:02d}.txt"
            self.assertEqual(meta['source'], expected_filename)
