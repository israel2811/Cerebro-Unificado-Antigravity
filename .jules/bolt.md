# Bolt's Performance Journal

## 2025-04-19 - Batching and Heuristics in Vector Indexing
**Learning:** Performing expensive string operations like `.split()` inside high-frequency loops (e.g., during document indexing) can become a significant bottleneck. Additionally, individual database insertions (like `collection.add` in ChromaDB) incur high IPC/network overhead compared to batched operations.
**Action:** Always implement a lightweight pre-filter (like character length checks) before expensive text processing. Use batching for database writes to leverage vectorized computations and reduce overhead.
