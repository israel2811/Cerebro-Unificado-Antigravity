import unittest
import importlib.util
import sys

# Dynamically import 02_docs_prep_injector.py
spec = importlib.util.spec_from_file_location(
    "docs_prep_injector",
    "scripts_leviathan/02_docs_prep_injector.py"
)
prep_mod = importlib.util.module_from_spec(spec)
sys.modules["docs_prep_injector"] = prep_mod
spec.loader.exec_module(prep_mod)

class TestDocsPrepInjector(unittest.TestCase):
    def test_clean_brackets_basic(self):
        text = "Hello {World}! This is {a test}."
        expected = "Hello ! This is ."
        self.assertEqual(prep_mod.clean_brackets(text), expected)

    def test_clean_brackets_nested(self):
        text = "foo { bar { nested } baz } qux"
        expected = "foo  baz } qux"
        self.assertEqual(prep_mod.clean_brackets(text), expected)

    def test_clean_brackets_no_braces(self):
        text = "Hello World! No braces here."
        expected = "Hello World! No braces here."
        self.assertEqual(prep_mod.clean_brackets(text), expected)

    def test_clean_brackets_unbalanced_open(self):
        text = "Hello {World"
        expected = "Hello {World"
        self.assertEqual(prep_mod.clean_brackets(text), expected)

    def test_clean_brackets_unbalanced_close(self):
        text = "Hello World}"
        expected = "Hello World}"
        self.assertEqual(prep_mod.clean_brackets(text), expected)

    def test_clean_html_noise(self):
        html_input = "<html><body><p>Hello <b>World</b>!</p>{JSON_DATA}</body></html>"
        expected = "Hello \nWorld\n!\n"
        self.assertEqual(prep_mod.clean_html_noise(html_input), expected)

if __name__ == '__main__':
    unittest.main()
