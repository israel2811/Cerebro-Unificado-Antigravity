## 2025-04-08 - Optimized Vector Indexing with Batching and Pre-filtering
**Learning:** For vector databases like ChromaDB, inserting documents in batches (e.g., BATCH_SIZE=50) significantly reduces IPC/network overhead and leverages vectorized embedding operations. Additionally, using `len(string)` as a pre-filter before expensive operations like `.split()` avoids unnecessary memory allocation and CPU cycles for small inputs.
**Action:** Always implement batching for database/API writes and use cheap length checks before expensive text processing in data pipelines.
