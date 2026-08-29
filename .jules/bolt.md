## 2025-05-15 - Batching ChromaDB Indexing for Performance and Memory Efficiency
**Learning:** In resource-constrained environments (2GB RAM), individual vector database insertions are not just slow but also memory-inefficient due to repeated IPC and single-item embedding calls. Using a string length pre-filter (`len()`) before `split()` is critical to avoid unnecessary large list allocations.
**Action:** Always implement batching (e.g., BATCH_SIZE = 50) for vector indexing and use O(1) checks before O(n) data transformations to stay within memory limits.
