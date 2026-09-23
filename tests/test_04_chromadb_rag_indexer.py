import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import tempfile
import importlib.util

class TestChromaDBRAGIndexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock chromadb in sys.modules before importing the script
        cls.mock_chromadb = MagicMock()
        cls.mock_embedding = MagicMock()
        cls.mock_chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction.return_value = cls.mock_embedding
        sys.modules["chromadb"] = cls.mock_chromadb
        sys.modules["chromadb.utils"] = cls.mock_chromadb.utils
        sys.modules["chromadb.utils.embedding_functions"] = cls.mock_chromadb.utils.embedding_functions

        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "04_chromadb_rag_indexer.py")
        )
        spec = importlib.util.spec_from_file_location("chroma_rag_indexer", script_path)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_word_truncation_maxsplit(self):
        # Test word truncation using split(None, 40000)
        large_text = "word " * 50000
        words = large_text.split(None, 40000)
        self.assertEqual(len(words), 40001)

        truncated = " ".join(words[:40000])
        self.assertEqual(len(truncated.split()), 40000)

    def test_local_chroma_rag_inject_batching(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create 25 text files in temporary directory
            for i in range(1, 26):
                file_path = os.path.join(temp_dir, f"chunk_{i:02d}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"This is chunk number {i} content.")

            mock_collection = MagicMock()
            mock_client = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            self.mock_chromadb.PersistentClient.return_value = mock_client

            with patch.object(self.module, "CLEAN_CHUNKS_DIR", temp_dir):
                self.module.local_chroma_rag_inject()

            # Expect collection.add to be called twice: 1st batch of 20, 2nd batch of 5
            self.assertEqual(mock_collection.add.call_count, 2)

            first_call_args = mock_collection.add.call_args_list[0][1]
            self.assertEqual(len(first_call_args["documents"]), 20)
            self.assertEqual(len(first_call_args["ids"]), 20)
            self.assertEqual(len(first_call_args["metadatas"]), 20)

            second_call_args = mock_collection.add.call_args_list[1][1]
            self.assertEqual(len(second_call_args["documents"]), 5)
            self.assertEqual(len(second_call_args["ids"]), 5)
            self.assertEqual(len(second_call_args["metadatas"]), 5)

if __name__ == "__main__":
    unittest.main()
