import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Inject fake chromadb module if chromadb is not installed
if 'chromadb' not in sys.modules:
    mock_chromadb = MagicMock()
    sys.modules['chromadb'] = mock_chromadb
    sys.modules['chromadb.utils'] = MagicMock()
    sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

import importlib
indexer = importlib.import_module("scripts_leviathan.04_chromadb_rag_indexer")

class TestChromaDBRAGIndexer(unittest.TestCase):

    def test_word_truncation_maxsplit(self):
        """Verify that split(None, 40000) truncates texts with > 40k words accurately."""
        large_text = "word " * 50000
        words = large_text.split(None, 40000)
        self.assertGreater(len(words), 40000)
        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    @patch.object(indexer, "chromadb")
    def test_local_chroma_rag_inject_batching(self, mock_chroma):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chroma.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        with tempfile.TemporaryDirectory() as temp_dir:
            chunks_dir = os.path.join(temp_dir, "clean_chunks")
            db_dir = os.path.join(temp_dir, "nexus_vector_db")
            os.makedirs(chunks_dir, exist_ok=True)

            # Create 25 test chunk files to verify batch size of 20 (batch 1: 20 items, batch 2: 5 items)
            for i in range(1, 26):
                file_path = os.path.join(chunks_dir, f"chunk_{i:02d}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"This is chunk number {i}")

            with patch.object(indexer, "CLEAN_CHUNKS_DIR", chunks_dir), \
                 patch.object(indexer, "DB_PATH", db_dir):
                indexer.local_chroma_rag_inject()

            # Verify collection.add was called twice (batch 1: 20 docs, batch 2: 5 docs)
            self.assertEqual(mock_collection.add.call_count, 2)

            # First batch assertions
            first_call_args = mock_collection.add.call_args_list[0][1]
            self.assertEqual(len(first_call_args["documents"]), 20)
            self.assertEqual(len(first_call_args["ids"]), 20)
            self.assertEqual(len(first_call_args["metadatas"]), 20)

            # Second batch assertions
            second_call_args = mock_collection.add.call_args_list[1][1]
            self.assertEqual(len(second_call_args["documents"]), 5)
            self.assertEqual(len(second_call_args["ids"]), 5)
            self.assertEqual(len(second_call_args["metadatas"]), 5)

    @patch.object(indexer, "chromadb")
    def test_local_chroma_rag_inject_missing_dir(self, mock_chroma):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chroma.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        non_existent_dir = "/tmp/non_existent_chunks_directory_xyz_123"
        with patch.object(indexer, "CLEAN_CHUNKS_DIR", non_existent_dir):
            indexer.local_chroma_rag_inject()

        # Add should not be called if directory does not exist
        mock_collection.add.assert_not_called()


if __name__ == "__main__":
    unittest.main()
