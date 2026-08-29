import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import importlib.util

class Test04ChromaDBRagIndexer(unittest.TestCase):
    def setUp(self):
        # 1. Mock chromadb inside sys.modules before importing the module
        self.mock_chromadb = MagicMock()
        self.mock_client = MagicMock()
        self.mock_collection = MagicMock()

        self.mock_chromadb.PersistentClient.return_value = self.mock_client
        self.mock_client.get_or_create_collection.return_value = self.mock_collection

        sys.modules['chromadb'] = self.mock_chromadb
        sys.modules['chromadb.utils'] = MagicMock()

        # 2. Dynamically load the module using importlib
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts_leviathan",
            "04_chromadb_rag_indexer.py"
        )
        spec = importlib.util.spec_from_file_location("indexer", script_path)
        self.indexer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.indexer_module)

        # Save original directories
        self.original_clean_chunks_dir = self.indexer_module.CLEAN_CHUNKS_DIR
        self.original_db_path = self.indexer_module.DB_PATH

    def tearDown(self):
        # Restore sys.modules
        sys.modules.pop('chromadb', None)
        sys.modules.pop('chromadb.utils', None)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open')
    def test_batching_and_split_optimization(self, mock_open, mock_listdir, mock_exists):
        # Set exists to True for CLEAN_CHUNKS_DIR
        mock_exists.return_value = True

        # Simulate 25 txt files (to verify BATCH_SIZE = 20 splits properly into 20 and 5)
        # Shuffled to verify alphabetical sorting in the code
        files = [f"chapter_{i}.txt" for i in range(1, 26)]
        files_shuffled = sorted(files, reverse=True)
        mock_listdir.return_value = files_shuffled

        # We need to simulate file reads. To verify the truncation logic,
        # let's make chapter_1.txt have more than 40000 words.
        long_content = "word " * 50000
        normal_content = "word " * 10

        # When opening, we return file handles that yield these contents
        file_mocks = {}
        for f in files:
            m = MagicMock()
            # __enter__ and __exit__ for with statement
            m.__enter__.return_value = m
            if f == "chapter_1.txt":
                m.read.return_value = long_content
            else:
                m.read.return_value = normal_content
            file_mocks[f] = m

        # mock_open returns the respective mocks in sequence
        mock_open.side_effect = lambda filepath, mode, encoding=None: file_mocks[os.path.basename(filepath)]

        # 3. Configure mock collection.add with a side_effect to copy the mutable lists
        # because the original lists are cleared in the finally block.
        recorded_calls = []
        def collection_add_side_effect(*args, **kwargs):
            recorded_calls.append({
                "documents": list(kwargs.get("documents", [])),
                "metadatas": list(kwargs.get("metadatas", [])),
                "ids": list(kwargs.get("ids", []))
            })
            return MagicMock()

        self.mock_collection.add.side_effect = collection_add_side_effect

        # Run the injector
        self.indexer_module.local_chroma_rag_inject()

        # Assertions
        # 1. Total batch runs must be 2 (first batch of 20, second batch of 5)
        self.assertEqual(len(recorded_calls), 2)

        # First batch should have 20 items
        self.assertEqual(len(recorded_calls[0]["documents"]), 20)
        # Second batch should have 5 items
        self.assertEqual(len(recorded_calls[1]["documents"]), 5)

        # We sorted them inside the code, so files should be indexed alphabetically (lexicographical order)
        # Let's verify IDs in order
        all_ids = recorded_calls[0]["ids"] + recorded_calls[1]["ids"]
        expected_files = sorted(files)
        expected_ids = [f"chunk_{i}_{archivo}" for i, archivo in enumerate(expected_files, 1)]
        self.assertEqual(all_ids, expected_ids)

        # Chapter 1 should be truncated to exactly 40000 words
        # and not have more.
        chap1_id = None
        for cid in all_ids:
            if "chapter_1.txt" in cid:
                chap1_id = cid
                break

        self.assertIsNotNone(chap1_id)
        chap1_doc = None
        for call in recorded_calls:
            if chap1_id in call["ids"]:
                idx = call["ids"].index(chap1_id)
                chap1_doc = call["documents"][idx]
                break

        self.assertIsNotNone(chap1_doc)
        # It must have been truncated to 40000 words
        self.assertEqual(len(chap1_doc.split()), 40000)

if __name__ == '__main__':
    unittest.main()
