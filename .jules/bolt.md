# Bolt's Performance Journal ⚡

## 2026-05-11 - Optimizing ChromaDB Indexing and String Processing
**Learning:** Using `str.split()` on large strings (e.g., 15MB corpus) in a loop creates massive in-memory lists, causing significant CPU and memory overhead (~2.0s for 15MB). Using `str.split(None, maxsplit)` combined with a character-length heuristic pre-filter (checking `len(s)` before `split`) reduces processing time to milliseconds (~0.14s, a 14x improvement). Additionally, batching database insertions (e.g., `collection.add` in ChromaDB) significantly reduces IPC and disk I/O overhead compared to per-document insertion.

**Action:** Always use character-length heuristics as a fast pre-filter for expensive string operations. Use `maxsplit` when only a prefix of words is needed. Implement batching for all database or API write operations to maximize throughput. Use `finally` blocks to ensure batch state is cleared after errors to prevent "poisoned" subsequent batches.
