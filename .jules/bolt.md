## 2026-07-15 - [Efficient Truncation and Batching in ChromaDB Indexing]
**Learning:** For large text processing, using `split(None, maxsplit)` is significantly faster (~5.7x) than a full `split()` when only a prefix word count is needed. Implementing batching for `collection.add` reduces simulated overhead by 20x for 100 documents.
**Action:** Always prefer `maxsplit` for length-based truncation and implement batching for vector database insertions to minimize I/O overhead.
