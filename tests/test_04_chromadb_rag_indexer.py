import os
import sys
import unittest
import importlib
from unittest.mock import MagicMock, patch

# Ensure sys.path includes repository root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Inject mock chromadb into sys.modules if chromadb is not installed
mock_chroma = MagicMock()
mock_embedding_funcs = MagicMock()
mock_chroma.utils.embedding_functions = mock_embedding_funcs

sys.modules.setdefault("chromadb", mock_chroma)
sys.modules.setdefault("chromadb.utils", mock_chroma.utils)
sys.modules.setdefault("chromadb.utils.embedding_functions", mock_embedding_funcs)

class TestChromaDBRAGIndexer(unittest.TestCase):

    def test_word_splitting_truncation(self):
        """Test that single-pass split(None, 40001) correctly truncates content over 40000 words."""
        # Create string with 50,000 words
        words_input = ["word" + str(i) for i in range(50000)]
        content = " ".join(words_input)

        words = content.split(None, 40001)
        self.assertGreater(len(words), 40000)

        truncated_content = " ".join(words[:40000])
        self.assertEqual(len(truncated_content.split()), 40000)
        self.assertEqual(words[0], "word0")
        self.assertEqual(words[39999], "word39999")

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("builtins.open")
    def test_batch_indexing_and_sorting(self, mock_open, mock_listdir, mock_exists):
        """Test that local_chroma_rag_inject sorts files and adds documents in batches of 20."""
        # Setup Chroma client mock
        mock_collection = MagicMock()
        mock_client_inst = MagicMock()
        mock_client_inst.get_or_create_collection.return_value = mock_collection
        mock_chroma.PersistentClient.return_value = mock_client_inst

        # Load indexer module dynamically
        indexer_module = importlib.import_module("scripts_leviathan.04_chromadb_rag_indexer")

        # Setup OS mocks
        mock_exists.return_value = True
        # Provide unsorted list of files: chunk_2, chunk_1, chunk_3, chunk_10, chunk_4...
        unsorted_files = ["chunk_2.txt", "chunk_1.txt", "chunk_3.txt"] + [f"chunk_{i}.txt" for i in range(4, 25)]
        mock_listdir.return_value = unsorted_files

        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = "Sample chunk content text"
        mock_open.return_value.__enter__.return_value = mock_file

        # Run indexer function
        indexer_module.local_chroma_rag_inject()

        # Check collection.add calls: 24 files total, batch size 20 => 1 batch of 20, 1 batch of 4
        self.assertEqual(mock_collection.add.call_count, 2)

        # Verify first call had 20 documents
        first_call_args = mock_collection.add.call_args_list[0][1]
        self.assertEqual(len(first_call_args["documents"]), 20)
        self.assertEqual(len(first_call_args["ids"]), 20)

        # Verify second call had 4 documents (remaining)
        second_call_args = mock_collection.add.call_args_list[1][1]
        self.assertEqual(len(second_call_args["documents"]), 4)
        self.assertEqual(len(second_call_args["ids"]), 4)

        # Verify sorting: chunk_1.txt should be the first file processed
        self.assertTrue(first_call_args["ids"][0].endswith("chunk_1.txt"))

if __name__ == "__main__":
    unittest.main()
