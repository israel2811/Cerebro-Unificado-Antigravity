## 2026-05-19 - Optimization of Large Text Indexing in ChromaDB

**Learning:** Performing a full `.split()` on large text buffers (e.g., 17MB corpus chunks) to count words or truncate is extremely expensive in Python, especially when done multiple times. The original logic was creating massive intermediate lists, consuming significant CPU and memory. Additionally, single-document insertions into a vector database incur high IPC and transaction overhead.

**Action:** Always use `str.split(None, maxsplit)` when only a specific number of words are needed. Use a character-length heuristic (`len(text) > threshold`) as a fast pre-filter before any splitting. Implement batching (e.g., `BATCH_SIZE=50`) for all database ingestion tasks to minimize overhead, and ensure batch state is cleared in a `finally` block to prevent "poisoned batches" on failure.
