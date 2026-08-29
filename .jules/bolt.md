## 2026-06-04 - Optimized Word Truncation and Batching in ChromaDB Indexer
**Learning:** Using `split(None, N+1)` (with `maxsplit`) instead of `split()[:N]` for word-count truncation provides a massive speedup (~120x for 1M words, ~3x for 100k words) because it avoids tokenizing the entire string when only a prefix is needed. Additionally, batching `collection.add()` calls in ChromaDB significantly reduces transaction overhead.
**Action:** Always use `maxsplit` when checking or truncating word counts in large text buffers. Implement batching for database insertions to minimize network/disk overhead.

**Learning:** `unittest.mock.patch` fails with `ValueError: invalid format` when targeting modules with numeric prefixes in their filenames (e.g., `04_chromadb_rag_indexer.py`) because they are not valid Python identifiers.
**Action:** Use `importlib.util` to load such scripts as modules and manually override attributes for testing instead of using `@patch` on the module path.
