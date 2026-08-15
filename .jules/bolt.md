## 2025-04-04 - [Batching for Vector Database Indexing]
**Learning:** For vector database indexing (ChromaDB), using batching (e.g., BATCH_SIZE = 50) significantly optimizes network/IPC overhead and enables vectorized embedding operations. In environments with limited RAM (2GB), efficient string handling and batching are critical to prevent OOM errors and minimize processing time.
**Action:** Always implement batch processing for `collection.add` or similar operations, include a 'flush' step after main loops, and use try-finally blocks to ensure state is cleared.
