import unittest
import os
import sys
import tempfile
import shutil
import importlib
from unittest.mock import MagicMock, patch, call

class TestChromaDBRAGIndexer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.chunks_dir = os.path.join(self.temp_dir, "clean_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_truncation_logic(self):
        """Verify that split(None, 40000) limits words to 40,000 without full-string tokenization overhead."""
        large_text = "word " * 50000
        words = large_text.split(None, 40000)
        self.assertGreater(len(words), 40000)
        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_local_chroma_rag_inject_batching(self, mock_listdir, mock_exists):
        """Test that local_chroma_rag_inject batches collection inserts into chunks of 20."""
        mock_exists.return_value = True
        # Create 25 mock txt files to test batch size of 20 + final batch of 5
        mock_files = [f"doc_{i:02d}.txt" for i in range(25)]
        mock_listdir.return_value = mock_files[::-1]  # Return unordered to test sorting

        mock_chroma_client = MagicMock()
        mock_collection = MagicMock()
        mock_chroma_client.get_or_create_collection.return_value = mock_collection

        mock_chromadb = MagicMock()
        mock_chromadb.PersistentClient.return_value = mock_chroma_client

        with patch.dict(sys.modules, {"chromadb": mock_chromadb, "chromadb.utils": MagicMock()}):
            indexer_module = importlib.import_module("scripts_leviathan.04_chromadb_rag_indexer")

            with patch("builtins.open", unittest.mock.mock_open(read_data="Sample content for testing")):
                with patch.object(indexer_module, "CLEAN_CHUNKS_DIR", self.chunks_dir):
                    indexer_module.local_chroma_rag_inject()

        # Should be called twice: once for 20 documents and once for 5 documents
        self.assertEqual(mock_collection.add.call_count, 2)
        first_call = mock_collection.add.call_args_list[0]
        second_call = mock_collection.add.call_args_list[1]

        self.assertEqual(len(first_call.kwargs["documents"]), 20)
        self.assertEqual(len(second_call.kwargs["documents"]), 5)

        # Verify sorted ordering: doc_00.txt should be the first document in the first batch
        self.assertEqual(first_call.kwargs["metadatas"][0]["source"], "doc_00.txt")

if __name__ == "__main__":
    unittest.main()
