## 2025-05-22 - [Vector Database Batching Optimization]
**Learning:** Inserting documents one by one into ChromaDB (or similar vector DBs) is significantly slower than batching. Batching reduces network/IPC overhead and enables the underlying embedding model to use vectorized operations (SIMD/GPU) for multiple documents simultaneously.
**Action:** Always use batching (e.g., `BATCH_SIZE = 50`) when performing mass injections into vector databases. Ensure the batch state is cleared in a `finally` block to prevent error cascades if a single batch fails.
