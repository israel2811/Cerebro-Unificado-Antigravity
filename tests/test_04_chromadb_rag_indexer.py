import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock chromadb in sys.modules if not installed
if "chromadb" not in sys.modules:
    mock_chroma = MagicMock()
    sys.modules["chromadb"] = mock_chroma
    sys.modules["chromadb.utils"] = MagicMock()
    sys.modules["chromadb.utils.embedding_functions"] = MagicMock()

class TestChromaDBRAGIndexerOptimization(unittest.TestCase):

    def test_split_maxsplit_truncation_correctness(self):
        """Verify that split(None, 40001) produces identical results to full splitting for truncation."""
        words_sample = ["word" + str(i) for i in range(50000)]
        text = " ".join(words_sample)

        # Original approach
        orig_words = text.split()
        if len(orig_words) > 40000:
            orig_result = " ".join(orig_words[:40000])
        else:
            orig_result = text

        # Optimized approach
        opt_words = text.split(None, 40001)
        if len(opt_words) > 40000:
            opt_result = " ".join(opt_words[:40000])
        else:
            opt_result = text

        self.assertEqual(orig_result, opt_result)
        self.assertEqual(len(opt_result.split()), 40000)

    def test_split_maxsplit_under_limit(self):
        """Verify behavior when word count is below the truncation limit."""
        words_sample = ["word" + str(i) for i in range(100)]
        text = " ".join(words_sample)

        opt_words = text.split(None, 40001)
        if len(opt_words) > 40000:
            opt_result = " ".join(opt_words[:40000])
        else:
            opt_result = text

        self.assertEqual(text, opt_result)

    def test_batch_indexing(self):
        """Verify that documents are indexed in batches of size 20."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        sys.modules["chromadb"].PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # Import module dynamically or safely
        import importlib.util
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts_leviathan",
            "04_chromadb_rag_indexer.py"
        )

        spec = importlib.util.spec_from_file_location("rag_indexer", script_path)
        rag_indexer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rag_indexer)

        # Create temporary directory with 25 text files
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            rag_indexer.CLEAN_CHUNKS_DIR = temp_dir
            for i in range(1, 26):
                file_path = os.path.join(temp_dir, f"chunk_{i}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Sample content for chunk {i}")

            rag_indexer.local_chroma_rag_inject()

            # Should be called twice: 1st call with 20 items, 2nd call with 5 items
            self.assertEqual(mock_collection.add.call_count, 2)

            first_call_args = mock_collection.add.call_args_list[0][1]
            second_call_args = mock_collection.add.call_args_list[1][1]

            self.assertEqual(len(first_call_args["documents"]), 20)
            self.assertEqual(len(second_call_args["documents"]), 5)

if __name__ == "__main__":
    unittest.main()
