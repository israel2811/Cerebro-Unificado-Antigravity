## 2026-06-05 - [Batching and Efficient Truncation in ChromaDB Indexer]
**Learning:** Batching `collection.add()` calls in ChromaDB significantly reduces overhead compared to individual insertions. Using `split(None, N+1)` for word-count truncation is orders of magnitude faster than full `split()` followed by slicing, as it avoids unnecessary memory allocation for the entire string.
**Action:** Always implement batching for vector database insertions. Use `maxsplit` in string operations when only a prefix or a limit is needed to optimize CPU and memory usage.
