import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts_leviathan import nexus_batch_worker


class TestNexusBatchWorker(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_root = nexus_batch_worker.ROOT
        self.old_out = nexus_batch_worker.OUT

        nexus_batch_worker.ROOT = self.test_dir
        nexus_batch_worker.OUT = self.test_dir / ".nexus-artifacts"

    def tearDown(self):
        nexus_batch_worker.ROOT = self.old_root
        nexus_batch_worker.OUT = self.old_out
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_mode_split_corpus(self):
        # Create a sample corpus file
        sample_file = self.test_dir / "sample_corpus.txt"
        lines = [f"Line {i}: " + ("x" * 100) + "\n" for i in range(500)]
        sample_file.write_text("".join(lines), encoding="utf-8")

        # Run mode_split_corpus with 1MB chunk limit (will force multiple chunks or small limit)
        # Using chunk_mb = 1 (1MB threshold)
        result = nexus_batch_worker.mode_split_corpus("sample_corpus.txt", chunk_mb=1)

        self.assertEqual(result["source"], "sample_corpus.txt")
        self.assertTrue(result["chunk_count"] >= 1)

        manifest_path = self.test_dir / result["manifest"]
        self.assertTrue(manifest_path.exists())

        manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest_data), result["chunk_count"])

        # Verify chunk file exists and sha256 / byte count matches
        for item in manifest_data:
            chunk_file = self.test_dir / item["path"]
            self.assertTrue(chunk_file.exists())
            data = chunk_file.read_bytes()
            self.assertEqual(len(data), item["bytes"])
            expected_sha = hashlib.sha256(data).hexdigest()
            self.assertEqual(expected_sha, item["sha256"])


if __name__ == "__main__":
    unittest.main()
