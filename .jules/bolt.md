## 2026-06-15 - Batch Indexing & Efficient Truncation
**Learning:** In resource-constrained environments (2GB RAM), individual database calls for ChromaDB indexing introduce significant overhead. Batching reduces this overhead proportionally to the batch size. Additionally, `str.split()` on large strings for word-count checks is expensive (O(N)); using `maxsplit` in `split(None, K)` reduces this to O(K), providing a massive speedup for large documents.
**Action:** Always batch vector database insertions and use `maxsplit` for early-exit string operations on large corpora.
