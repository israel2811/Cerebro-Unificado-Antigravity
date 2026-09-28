import os
import sys
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Inyectar mock de chromadb en sys.modules si no está instalado
if "chromadb" not in sys.modules:
    chromadb_mock = MagicMock()
    sys.modules["chromadb"] = chromadb_mock
    sys.modules["chromadb.utils"] = MagicMock()
    sys.modules["chromadb.utils.embedding_functions"] = MagicMock()

import importlib
indexer = importlib.import_module("scripts_leviathan.04_chromadb_rag_indexer")


class TestChromaDBRAGIndexer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.chunks_dir = os.path.join(self.temp_dir, "clean_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_local_chroma_rag_inject_batching_and_truncation(self):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        # Crear 25 archivos de chunk para probar el procesamiento en lotes (20 + 5)
        for i in range(1, 26):
            filename = f"chunk_{i:02d}.txt"
            filepath = os.path.join(self.chunks_dir, filename)
            if i == 1:
                # Archivo con > 40,000 palabras para probar la truncación con maxsplit
                content = "word " * 45000
            else:
                content = f"content of chunk {i}"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

        with patch.object(indexer, "CLEAN_CHUNKS_DIR", self.chunks_dir), \
             patch("chromadb.PersistentClient", return_value=mock_client):

            indexer.local_chroma_rag_inject()

        # Verificar que collection.add fue llamado 2 veces (un lote de 20 y luego 5)
        self.assertEqual(mock_collection.add.call_count, 2)

        # Verificar el primer lote de 20
        first_call = mock_collection.add.call_args_list[0]
        _, kwargs1 = first_call
        self.assertEqual(len(kwargs1["documents"]), 20)
        self.assertEqual(len(kwargs1["ids"]), 20)
        self.assertEqual(len(kwargs1["metadatas"]), 20)

        # Verificar que el primer documento fue truncado a exactamente 40,000 palabras
        first_doc = kwargs1["documents"][0]
        word_count = len(first_doc.split())
        self.assertEqual(word_count, 40000)

        # Verificar el segundo lote de 5
        second_call = mock_collection.add.call_args_list[1]
        _, kwargs2 = second_call
        self.assertEqual(len(kwargs2["documents"]), 5)

    def test_empty_chunks_directory(self):
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        with patch.object(indexer, "CLEAN_CHUNKS_DIR", self.chunks_dir), \
             patch("chromadb.PersistentClient", return_value=mock_client):

            indexer.local_chroma_rag_inject()

        mock_collection.add.assert_not_called()


if __name__ == "__main__":
    unittest.main()
