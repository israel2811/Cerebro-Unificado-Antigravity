
## 2026-07-12 - [Optimized ChromaDB Indexing]
**Learning:** Redundant `split()` calls on large strings are O(N) bottlenecks. Using `maxsplit` in `split(None, LIMIT)` avoids full-string processing when only a prefix is needed. Additionally, single-document vector insertions suffer from high API/process overhead.
**Action:** Always prefer batching for vector database insertions and use `maxsplit` for early-exit string processing in Python.
