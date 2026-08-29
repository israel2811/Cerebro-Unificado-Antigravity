## 2026-05-21 - Efficient String Truncation and Batching in ChromaDB Indexer

**Learning:** Using `str.split()` without `maxsplit` on large text buffers (e.g., 17MB corpus chunks) to check word counts creates massive temporary lists in memory and consumes significant CPU cycles. Additionally, inserting documents into ChromaDB one-by-one incurs high overhead due to repeated disk I/O and internal indexing triggers.

**Action:** Always use a character-length heuristic (e.g., `len(text) > threshold`) as a fast-path pre-filter before word-based checks. Use `split(None, maxsplit)` when truncating to avoid processing the entire buffer. Implement batch insertion (e.g., `BATCH_SIZE=50`) for vector databases to amortize indexing overhead.
