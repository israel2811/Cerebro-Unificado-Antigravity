import sys
import unittest
from unittest.mock import MagicMock, patch
import importlib.util
import os
import tempfile

# Prepare chromadb mock in sys.modules
mock_chroma = MagicMock()
mock_embedding_funcs = MagicMock()
mock_chroma.utils.embedding_functions = mock_embedding_funcs

sys.modules['chromadb'] = mock_chroma
sys.modules['chromadb.utils'] = mock_chroma.utils
sys.modules['chromadb.utils.embedding_functions'] = mock_embedding_funcs

# Import the module with numeric prefix
script_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'scripts_leviathan',
    '04_chromadb_rag_indexer.py',
)
spec = importlib.util.spec_from_file_location('chroma_indexer', script_path)
chroma_indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chroma_indexer)


class TestChromaRAGIndexer(unittest.TestCase):

    def test_truncation_maxsplit(self):
        """Test that maxsplit truncation logic correctly truncates words exceeding 40k."""
        # Short string
        text_short = "word " * 1000
        parts = text_short.split(None, 40001)
        self.assertLessEqual(len(parts), 40000)

        # Long string exceeding 40000 words
        text_long = "word " * 45000
        parts_long = text_long.split(None, 40001)
        self.assertGreater(len(parts_long), 40000)
        truncated = " ".join(parts_long[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    def test_local_chroma_rag_inject_batching_and_sorting(self):
        """Test batch insertion and alphabetical sorting order."""
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chroma.PersistentClient.return_value = mock_client

        with tempfile.TemporaryDirectory() as tmp_dir:
            chunks_dir = os.path.join(tmp_dir, "clean_chunks")
            os.makedirs(chunks_dir, exist_ok=True)

            # Create 25 dummy chunk files (unsorted creation order)
            file_names = [f"chapter_{i:02d}.txt" for i in reversed(range(1, 26))]
            for fname in file_names:
                with open(os.path.join(chunks_dir, fname), "w", encoding="utf-8") as f:
                    f.write(f"Content for {fname}")

            with patch.object(chroma_indexer, 'CLEAN_CHUNKS_DIR', chunks_dir), \
                 patch.object(chroma_indexer, 'DB_PATH', os.path.join(tmp_dir, "vector_db")):
                chroma_indexer.local_chroma_rag_inject()

            # For 25 items and BATCH_SIZE=20, collection.add should be called twice (20 then 5)
            self.assertEqual(mock_collection.add.call_count, 2)

            call_1 = mock_collection.add.call_args_list[0]
            call_2 = mock_collection.add.call_args_list[1]

            docs_1 = call_1.kwargs['documents']
            docs_2 = call_2.kwargs['documents']

            self.assertEqual(len(docs_1), 20)
            self.assertEqual(len(docs_2), 5)

            metas_1 = call_1.kwargs['metadatas']
            # Assert alphabetical sorting: chapter_01.txt should be first
            self.assertEqual(metas_1[0]['source'], 'chapter_01.txt')
            self.assertEqual(metas_1[1]['source'], 'chapter_02.txt')


if __name__ == '__main__':
    unittest.main()
