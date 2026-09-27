import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Ensure sys.modules has chromadb mocked if chromadb is not installed
mock_chroma = MagicMock()
mock_embedding = MagicMock()
if "chromadb" not in sys.modules:
    sys.modules["chromadb"] = mock_chroma
    sys.modules["chromadb.utils"] = MagicMock()
    sys.modules["chromadb.utils.embedding_functions"] = mock_embedding

# Add scripts_leviathan directory to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan"))

import importlib
chroma_indexer = importlib.import_module("04_chromadb_rag_indexer")


class TestChromaRAGIndexer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.chunks_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_local_chroma_rag_inject_batching(self):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        # Create 25 dummy txt files
        for i in range(1, 26):
            filename = f"doc_{i:02d}.txt"
            filepath = os.path.join(self.chunks_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Sample content for file {i}")

        with patch.object(chroma_indexer.chromadb, "PersistentClient", return_value=mock_client), \
             patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", self.chunks_dir):
            chroma_indexer.local_chroma_rag_inject()

        # Should be called twice: 1st call batch of 20, 2nd call batch of 5
        self.assertEqual(mock_collection.add.call_count, 2)

        # Check 1st call had 20 documents
        first_call_args = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_args["documents"]), 20)
        self.assertEqual(len(first_call_args["ids"]), 20)
        self.assertEqual(len(first_call_args["metadatas"]), 20)

        # Check 2nd call had 5 documents
        second_call_args = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_args["documents"]), 5)
        self.assertEqual(len(second_call_args["ids"]), 5)

    def test_sorted_processing(self):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        # Create files out of alphabetical order
        filenames = ["chapter_b.txt", "chapter_a.txt", "chapter_c.txt"]
        for fn in filenames:
            with open(os.path.join(self.chunks_dir, fn), "w", encoding="utf-8") as f:
                f.write(f"Content for {fn}")

        with patch.object(chroma_indexer.chromadb, "PersistentClient", return_value=mock_client), \
             patch.object(chroma_indexer, "CLEAN_CHUNKS_DIR", self.chunks_dir):
            chroma_indexer.local_chroma_rag_inject()

        self.assertEqual(mock_collection.add.call_count, 1)
        added_metas = mock_collection.add.call_args[1]["metadatas"]
        sources = [meta["source"] for meta in added_metas]
        self.assertEqual(sources, ["chapter_a.txt", "chapter_b.txt", "chapter_c.txt"])


if __name__ == "__main__":
    unittest.main()
