import os
import sys
import unittest
import tempfile
import importlib
from unittest.mock import MagicMock, patch

# Ensure chromadb is mocked in sys.modules prior to loading the indexer script
mock_chromadb = MagicMock()
sys.modules['chromadb'] = mock_chromadb
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

# Import the indexer module dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
spec = importlib.util.find_spec("scripts_leviathan.04_chromadb_rag_indexer")
indexer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer_module)


class TestChromaRAGIndexer(unittest.TestCase):

    def test_truncation_large_file(self):
        """Test that files exceeding 40000 words are truncated to 40000 words."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Generate a text chunk with 45000 words
            large_text = "word " * 45000
            file_path = os.path.join(tmp_dir, "large_chunk.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(large_text)

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client

            with patch.object(indexer_module, "CLEAN_CHUNKS_DIR", tmp_dir):
                indexer_module.local_chroma_rag_inject()

            # Verify collection.add was called
            self.assertTrue(mock_collection.add.called)
            kwargs = mock_collection.add.call_args[1]
            added_doc = kwargs["documents"][0]
            word_count = len(added_doc.split())
            self.assertEqual(word_count, 40000)

    def test_normal_file_no_truncation(self):
        """Test that files with <= 40000 words are not truncated."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            normal_text = "hello world " * 100
            file_path = os.path.join(tmp_dir, "normal_chunk.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(normal_text)

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chromadb.PersistentClient.return_value = mock_client

            with patch.object(indexer_module, "CLEAN_CHUNKS_DIR", tmp_dir):
                indexer_module.local_chroma_rag_inject()

            self.assertTrue(mock_collection.add.called)
            kwargs = mock_collection.add.call_args[1]
            added_doc = kwargs["documents"][0]
            word_count = len(added_doc.split())
            self.assertEqual(word_count, 200)


if __name__ == "__main__":
    unittest.main()
