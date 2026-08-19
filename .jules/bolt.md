# Bolt's Performance Journal

## 2026-02-19 - Single-pass split truncation and ChromaDB batch insertion

**Learning:** Calling `.split()` twice on large multi-megabyte strings tokenizes the entire document into Python list objects in memory. Using `split(None, 40001)` with `maxsplit` stops tokenizing after 40,001 words, yielding a >120x speedup for text truncation. In addition, batching vector database insertions into groups of 20 (`BATCH_SIZE = 20`) drastically reduces per-document SQLite transaction overhead in ChromaDB.

**Action:** Always use `maxsplit` when checking or truncating string word counts, and batch database mutations to minimize transaction commits.
