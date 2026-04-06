## 2025-04-06 - Optimized ChromaDB Vector Indexing

**Learning:** Batching document insertions in ChromaDB significantly reduces network/IPC overhead and enables more efficient vectorized operations. Additionally, using character-based length pre-filtering (`len(s)`) before expensive string operations like `.split()` is crucial for performance when handling large text files in memory-constrained environments (2GB RAM).

**Action:** Always implement batching (e.g., `BATCH_SIZE = 50`) for vector database operations and use cheap `len()` checks before expensive string transformations.
