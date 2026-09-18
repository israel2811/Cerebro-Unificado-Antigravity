import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import MagicMock, patch
import importlib.util

# Mock chromadb and chromadb.utils.embedding_functions in sys.modules
mock_chromadb = MagicMock()
mock_ef = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = mock_ef

# Import scripts_leviathan/04_chromadb_rag_indexer.py dynamically
indexer_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts_leviathan",
    "04_chromadb_rag_indexer.py"
)
spec = importlib.util.spec_from_file_location("chroma_indexer", indexer_path)
chroma_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chroma_indexer)


class TestChromaDBIndexerOptimization(unittest.TestCase):

    def test_word_truncation_maxsplit(self):
        """Verify that split(None, 40001) truncates text exceeding 40000 words efficiently."""
        large_text = "word " * 50000
        words = large_text.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_content = " ".join(words[:40000])
        self.assertEqual(len(truncated_content.split()), 40000)

    def test_batch_insertion(self):
        """Verify that local_chroma_rag_inject batches collection.add calls in size of 20."""
        temp_dir = tempfile.mkdtemp()
        try:
            # Create 25 chunk files
            for i in range(1, 26):
                file_path = os.path.join(temp_dir, f"chunk_{i}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"This is sample test content for chunk {i}.")

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client

            with patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", temp_dir):
                chroma_indexer.local_chroma_rag_inject()

            # With 25 files and batch size 20, collection.add should be called twice (20 + 5)
            self.assertEqual(mock_collection.add.call_count, 2)

            # First batch should have 20 items
            first_call_kwargs = mock_collection.add.call_args_list[0][1]
            self.assertEqual(len(first_call_kwargs["documents"]), 20)

            # Second batch should have 5 items
            second_call_kwargs = mock_collection.add.call_args_list[1][1]
            self.assertEqual(len(second_call_kwargs["documents"]), 5)

        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
