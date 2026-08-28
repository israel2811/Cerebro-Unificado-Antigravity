import unittest
import os
import sys
import tempfile
import importlib.util

# Load 01_nexus_deep_scanner module dynamically
spec = importlib.util.spec_from_file_location(
    "nexus_deep_scanner",
    os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "01_nexus_deep_scanner.py")
)
nexus_deep_scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nexus_deep_scanner)

class TestNexusDeepScanner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.output_file.close()

    def tearDown(self):
        self.test_dir.cleanup()
        if os.path.exists(self.output_file.name):
            os.remove(self.output_file.name)

    def test_scan_and_extract_logic(self):
        # Create dummy test files in the temporary directory
        sub_dir = os.path.join(self.test_dir.name, "sub")
        os.makedirs(sub_dir, exist_ok=True)

        file1 = os.path.join(self.test_dir.name, "doc1.md")
        file2 = os.path.join(sub_dir, "doc2.txt")
        file_ignored = os.path.join(self.test_dir.name, "image.png")

        with open(file1, "w", encoding="utf-8") as f:
            f.write("Hello World from doc1!")

        with open(file2, "w", encoding="utf-8") as f:
            f.write("Hello World from doc2 with utf-8 chars: ñ, á, é, í, ó, ú!")

        with open(file_ignored, "w", encoding="utf-8") as f:
            f.write("Binary noise to ignore")

        # Override module variables for testing
        original_search_dirs = nexus_deep_scanner.SEARCH_DIRS
        original_output_file = nexus_deep_scanner.OUTPUT_FILE

        try:
            nexus_deep_scanner.SEARCH_DIRS = [self.test_dir.name]
            nexus_deep_scanner.OUTPUT_FILE = self.output_file.name

            nexus_deep_scanner.scan_and_extract()

            # Read result output
            with open(self.output_file.name, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(f"--- ORIGEN: {file1} ---", content)
            self.assertIn("Hello World from doc1!", content)
            self.assertIn(f"--- ORIGEN: {file2} ---", content)
            self.assertIn("Hello World from doc2 with utf-8 chars: ñ, á, é, í, ó, ú!", content)
            self.assertNotIn("Binary noise to ignore", content)

        finally:
            nexus_deep_scanner.SEARCH_DIRS = original_search_dirs
            nexus_deep_scanner.OUTPUT_FILE = original_output_file

if __name__ == "__main__":
    unittest.main()
