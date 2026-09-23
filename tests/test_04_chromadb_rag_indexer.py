import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import tempfile
import importlib

# Ensure tests can import module even if chromadb is not installed in the environment
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

# Dynamically import the numeric prefix python script
spec = importlib.util.spec_from_file_location(
    "chromadb_rag_indexer",
    os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
)
chromadb_rag_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chromadb_rag_indexer)


class TestChromaDBRAGIndexer(unittest.TestCase):

    @patch("chromadb.PersistentClient")
    def test_batching_and_sorting(self, mock_client_cls):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        with tempfile.TemporaryDirectory() as temp_dir:
            chunks_dir = os.path.join(temp_dir, "clean_chunks")
            os.makedirs(chunks_dir, exist_ok=True)

            # Create 25 mock chunk files to test batching with batch_size=20
            # Named chunk_10.txt, chunk_1.txt, etc., to verify alphabetical sorting
            filenames = [f"chunk_{i:02d}.txt" for i in range(1, 26)]
            for fname in filenames:
                with open(os.path.join(chunks_dir, fname), "w", encoding="utf-8") as f:
                    f.write(f"Sample content for {fname}")

            with patch.object(chromadb_rag_indexer, "CLEAN_CHUNKS_DIR", chunks_dir):
                chromadb_rag_indexer.local_chroma_rag_inject(batch_size=20)

            # Assert collection.add was called twice (batch of 20 and batch of 5)
            self.assertEqual(mock_collection.add.call_count, 2)

            # Check first call had 20 items
            first_call_args = mock_collection.add.call_args_list[0][1]
            self.assertEqual(len(first_call_args["documents"]), 20)
            self.assertEqual(first_call_args["metadatas"][0]["source"], "chunk_01.txt")
            self.assertEqual(first_call_args["ids"][0], "chunk_1_chunk_01.txt")

            # Check second call had 5 items
            second_call_args = mock_collection.add.call_args_list[1][1]
            self.assertEqual(len(second_call_args["documents"]), 5)
            self.assertEqual(second_call_args["metadatas"][-1]["source"], "chunk_25.txt")

    @patch("chromadb.PersistentClient")
    def test_truncation_large_file(self, mock_client_cls):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        with tempfile.TemporaryDirectory() as temp_dir:
            chunks_dir = os.path.join(temp_dir, "clean_chunks")
            os.makedirs(chunks_dir, exist_ok=True)

            # Create a large file with 45,000 words
            large_content = "word " * 45000
            with open(os.path.join(chunks_dir, "huge_chunk.txt"), "w", encoding="utf-8") as f:
                f.write(large_content)

            with patch.object(chromadb_rag_indexer, "CLEAN_CHUNKS_DIR", chunks_dir):
                chromadb_rag_indexer.local_chroma_rag_inject(batch_size=10)

            self.assertEqual(mock_collection.add.call_count, 1)
            call_args = mock_collection.add.call_args[1]
            processed_doc = call_args["documents"][0]
            word_count = len(processed_doc.split())
            self.assertEqual(word_count, 40000)


if __name__ == "__main__":
    unittest.main()
