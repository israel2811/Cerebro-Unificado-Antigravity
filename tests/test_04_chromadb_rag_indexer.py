import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import importlib.util

class TestChromaDBRAGIndexer(unittest.TestCase):
    def setUp(self):
        # Create temp dir for clean_chunks
        self.temp_dir = tempfile.TemporaryDirectory()
        self.chunks_dir = os.path.join(self.temp_dir.name, "clean_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

        # Mock chromadb in sys.modules
        self.mock_chroma = MagicMock()
        self.mock_client = MagicMock()
        self.mock_collection = MagicMock()

        self.mock_chroma.PersistentClient.return_value = self.mock_client
        self.mock_client.get_or_create_collection.return_value = self.mock_collection

        sys.modules['chromadb'] = self.mock_chroma
        sys.modules['chromadb.utils'] = MagicMock()
        sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

        # Dynamically import the script module
        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
        )
        spec = importlib.util.spec_from_file_location("chromadb_rag_indexer", script_path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_batching_and_sorting(self):
        # Create dummy text files
        for i in range(25):
            fname = f"chunk_{i:02d}.txt"
            fpath = os.path.join(self.chunks_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(f"Sample content for chunk {i}")

        # Patch CLEAN_CHUNKS_DIR
        with patch.object(self.module, "CLEAN_CHUNKS_DIR", self.chunks_dir):
            self.module.local_chroma_rag_inject()

        # For 25 items with BATCH_SIZE=20, collection.add should be called twice (batch 1: 20 items, batch 2: 5 items)
        self.assertEqual(self.mock_collection.add.call_count, 2)

        # Check first call arguments
        call1_kwargs = self.mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(call1_kwargs["documents"]), 20)
        self.assertEqual(len(call1_kwargs["ids"]), 20)

        # Check second call arguments
        call2_kwargs = self.mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(call2_kwargs["documents"]), 5)
        self.assertEqual(len(call2_kwargs["ids"]), 5)


if __name__ == "__main__":
    unittest.main()
