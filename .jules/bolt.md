# Bolt Journal

## 2025-05-14 - Batch Indexing & String Pre-filtering in ChromaDB
**Learning:** For vector database indexing (ChromaDB), use batching (e.g., BATCH_SIZE = 50) to optimize network/IPC overhead and enable vectorized embedding operations. Additionally, using a character-length heuristic (e.g., 150,000 chars) as a pre-filter before expensive string operations like `.split()` for word counting significantly reduces CPU usage for large files.
**Action:** Always implement batching for vector insertions and use fast pre-filters (like `len()`) before executing expensive string or array manipulations.
