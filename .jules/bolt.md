## 2026-06-06 - [ChromaDB Indexing Optimization]
**Learning:** Individual `collection.add()` calls in ChromaDB are much slower than batched calls due to transaction overhead. Additionally, word-count truncation using double `.split()` calls on large strings (1M+ words) is a significant bottleneck. Using `split(None, MAX_WORDS + 1)` provides a ~90x speedup for truncation.
**Action:** Always implement batching (e.g., BATCH_SIZE=20) for vector database insertions and use `maxsplit` in `split()` to avoid full-string processing when only a prefix is needed.
