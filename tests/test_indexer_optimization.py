import os
import sys
import unittest
from unittest.mock import MagicMock, patch, mock_open
import importlib.util

# 1. Manual injection of chromadb to sys.modules to satisfy dynamic loading
mock_chromadb = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()

# Load the target module dynamically since it has a numeric prefix '04_...'
module_name = "04_chromadb_rag_indexer"
module_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts_leviathan",
    "04_chromadb_rag_indexer.py"
)

spec = importlib.util.spec_from_file_location(module_name, module_path)
indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)

class TestIndexerOptimization(unittest.TestCase):
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_alphabetical_sorting_and_truncation(self, mock_listdir, mock_exists):
        # Setup mocks
        mock_exists.return_value = True

        # Unsorted list of chunks
        unordered_files = ["CORPUS_TESIS_VOL_12.txt", "CORPUS_TESIS_VOL_2.txt", "CORPUS_TESIS_VOL_1.txt", "CORPUS_TESIS_VOL_10.txt"]
        mock_listdir.return_value = unordered_files

        # Mock chromadb client & collection
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # Track inserted documents
        inserted_docs = {}
        def collection_add_side_effect(documents, metadatas, ids):
            for doc_id, doc, meta in zip(ids, documents, metadatas):
                inserted_docs[doc_id] = {
                    "document": doc,
                    "metadata": meta
                }
        mock_collection.add.side_effect = collection_add_side_effect

        # Mock file reading
        # Doc 1: has 45,000 words
        large_doc_content = " ".join(["word"] * 45000)
        # Doc 2: has 10 words
        small_doc_content = " ".join(["word"] * 10)

        file_contents = {
            os.path.join(indexer_module.CLEAN_CHUNKS_DIR, "CORPUS_TESIS_VOL_1.txt"): large_doc_content,
            os.path.join(indexer_module.CLEAN_CHUNKS_DIR, "CORPUS_TESIS_VOL_2.txt"): small_doc_content,
            os.path.join(indexer_module.CLEAN_CHUNKS_DIR, "CORPUS_TESIS_VOL_10.txt"): small_doc_content,
            os.path.join(indexer_module.CLEAN_CHUNKS_DIR, "CORPUS_TESIS_VOL_12.txt"): small_doc_content,
        }

        def mock_open_file(filepath, mode="r", encoding=None, errors=None):
            if filepath in file_contents:
                return mock_open(read_data=file_contents[filepath])()
            raise FileNotFoundError(filepath)

        with patch('builtins.open', side_effect=mock_open_file):
            indexer_module.local_chroma_rag_inject()

        # Assertion 1: Alphabetical / Lexicographical ordering
        # Sort of unordered_files: [VOL_1, VOL_10, VOL_12, VOL_2] lexicographically
        # Since files are processed in this alphabetical order:
        # chunk_1 should map to VOL_1
        # chunk_2 should map to VOL_10
        # chunk_3 should map to VOL_12
        # chunk_4 should map to VOL_2

        self.assertIn("chunk_1_CORPUS_TESIS_VOL_1.txt", inserted_docs)
        self.assertIn("chunk_2_CORPUS_TESIS_VOL_10.txt", inserted_docs)
        self.assertIn("chunk_3_CORPUS_TESIS_VOL_12.txt", inserted_docs)
        self.assertIn("chunk_4_CORPUS_TESIS_VOL_2.txt", inserted_docs)

        # Assertion 2: Word truncation logic (Doc 1 has 45,000 words, should be truncated to exactly 40,000)
        truncated_content = inserted_docs["chunk_1_CORPUS_TESIS_VOL_1.txt"]["document"]
        self.assertEqual(len(truncated_content.split()), 40000)

        # Doc 2 has 10 words, should NOT be truncated
        untruncated_content = inserted_docs["chunk_4_CORPUS_TESIS_VOL_2.txt"]["document"]
        self.assertEqual(len(untruncated_content.split()), 10)

if __name__ == '__main__':
    unittest.main()
