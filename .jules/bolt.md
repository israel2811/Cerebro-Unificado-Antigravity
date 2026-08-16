## 2026-05-16 - String Truncation and Batch Indexing Optimization
**Learning:** Using `str.split()` on large documents to count words is a massive performance bottleneck because it allocates a full list of words. Using a character-length heuristic as a pre-filter and `split(None, maxsplit)` can achieve >250x speedups. Additionally, vector database ingestion (ChromaDB) is significantly faster when batched, reducing the number of disk/network operations.
**Action:** Always use limited splits for truncation and batch writes for database ingestion.
