## 2025-05-15 - Vectorized Indexing Performance and String Efficiency
**Learning:** Redundant string operations like `.split()` on large datasets (100k+ words) cause significant CPU/memory overhead in limited RAM environments. Furthermore, single-item insertions into vector databases like ChromaDB incur high network/IPC overhead compared to batch operations.
**Action:** Implement batching (BATCH_SIZE = 50) for database insertions and use character-length pre-filters (e.g., len(text) > 150,000) to avoid expensive word-count splitting on smaller documents.
