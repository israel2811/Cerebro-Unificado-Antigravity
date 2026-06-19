## 2026-06-12 - Optimized ChromaDB Indexing with Batching and Efficient Truncation
**Learning:** Found two major bottlenecks in the RAG pipeline: 1) Individual `collection.add` calls incurred heavy overhead. 2) Using `len(s.split())` for truncation forced full-string tokenization.
**Action:** Implemented batching (size=20) and used `split(None, N+1)` for O(N) truncation instead of O(2N).
