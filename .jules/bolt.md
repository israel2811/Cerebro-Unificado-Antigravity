# Bolt's Journal - Performance Learnings

## 2026-02-17 - Maxsplit and Batching Optimization in ChromaDB Indexer
**Learning:** In text-indexing RAG pipelines, calling `split()` without `maxsplit` on large documents causes python to allocate a list for every word in memory. Using `split(None, 40001)` avoids full string tokenization when truncating. Additionally, batching ChromaDB `collection.add` calls reduces SQLite transaction overhead and vector model embedding batch overhead.
**Action:** Always prefer `split(sep, maxsplit)` for string truncation and batch vector insertions in RAG indexers.
