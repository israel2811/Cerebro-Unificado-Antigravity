import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import tempfile
import importlib.util

# Ensure chromadb and embedding_functions are mocked in sys.modules
mock_chromadb = MagicMock()
mock_utils = MagicMock()
mock_chromadb.utils = mock_utils
mock_ef = MagicMock()
mock_utils.embedding_functions = mock_ef

sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = mock_utils

class TestChromaDBRAGIndexer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.chunks_dir = os.path.join(self.temp_dir.name, "clean_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_truncation_logic(self):
        # Create a large document with 50,000 words
        large_text = "word " * 50000
        words = large_text.split(None, 40001)
        self.assertGreater(len(words), 40000)
        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    def test_local_chroma_rag_inject_batching(self):
        # Create 25 chunk files to trigger batching (BATCH_SIZE = 20)
        for i in range(1, 26):
            file_path = os.path.join(self.chunks_dir, f"chunk_{i:02d}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Sample content for chunk {i}")

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client

        # Dynamically import 04_chromadb_rag_indexer
        indexer_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
        )
        spec = importlib.util.spec_from_file_location("chroma_indexer", indexer_path)
        chroma_indexer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(chroma_indexer)

        # Patch CLEAN_CHUNKS_DIR
        with patch.object(chroma_indexer, 'CLEAN_CHUNKS_DIR', self.chunks_dir):
            chroma_indexer.local_chroma_rag_inject()

        # Check collection.add calls: 25 files should result in 2 batch calls (20 + 5)
        self.assertEqual(mock_collection.add.call_count, 2)

        first_call_args = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_args['documents']), 20)

        second_call_args = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_args['documents']), 5)

if __name__ == '__main__':
    unittest.main()
