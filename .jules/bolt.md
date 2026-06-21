## 2026-06-11 - Optimized Word Truncation and Batch Indexing
**Learning:** Using `split()` without `maxsplit` on large strings is extremely inefficient (O(N) where N is the number of words). `split(None, 40001)` is ~30x faster for a 1M word string. Also, batching database/vector store writes (e.g., ChromaDB) significantly reduces network/IO overhead.
**Action:** Always use `maxsplit` when only a prefix of words is needed from a large string. Implement batching for all collection/database write operations.
