import os
import sys
import unittest
import tempfile
import shutil
import importlib.util
from unittest.mock import MagicMock, patch

class TestChromaDBRAGIndexer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.chunks_dir = os.path.join(self.test_dir, "clean_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_truncation_logic(self):
        # Create text with 50,000 words
        large_text = "word " * 50000
        words = large_text.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_text = " ".join(words[:40000])
        self.assertEqual(len(truncated_text.split()), 40000)

    def test_batch_injection(self):
        # Prepare mock objects for chromadb
        mock_chroma = MagicMock()
        mock_utils = MagicMock()
        mock_ef = MagicMock()
        mock_utils.embedding_functions = mock_ef
        mock_chroma.utils = mock_utils

        mock_modules = {
            'chromadb': mock_chroma,
            'chromadb.utils': mock_utils,
            'chromadb.utils.embedding_functions': mock_ef
        }

        with patch.dict(sys.modules, mock_modules):
            # Import indexer module dynamically with mocked chromadb
            spec = importlib.util.spec_from_file_location(
                "rag_indexer",
                os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
            )
            rag_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(rag_module)

            # Create 25 dummy txt files to trigger 2 batches (20 + 5)
            for i in range(1, 26):
                chunk_file = os.path.join(self.chunks_dir, f"chunk_{i:02d}.txt")
                with open(chunk_file, "w", encoding="utf-8") as f:
                    f.write(f"Contenido del chunk {i}")

            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection

            with patch.object(rag_module.chromadb, 'PersistentClient', return_value=mock_client), \
                 patch.object(rag_module, 'CLEAN_CHUNKS_DIR', self.chunks_dir), \
                 patch.object(rag_module, 'DB_PATH', os.path.join(self.test_dir, "nexus_vector_db")):

                rag_module.local_chroma_rag_inject()

                # Verify collection.add was called twice: once for batch of 20, once for final flush of 5
                self.assertEqual(mock_collection.add.call_count, 2)

                # First batch check
                first_call_args = mock_collection.add.call_args_list[0][1]
                self.assertEqual(len(first_call_args['documents']), 20)

                # Second batch check
                second_call_args = mock_collection.add.call_args_list[1][1]
                self.assertEqual(len(second_call_args['documents']), 5)

if __name__ == "__main__":
    unittest.main()
