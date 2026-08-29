## 2026-06-26 - Optimized ChromaDB Indexer
**Learning:** Using `split(None, N+1)` is significantly faster than splitting an entire large string when only the first N words are needed. In benchmarks, it reduced processing time from ~1.18s to ~0.005s for a 10MB string. Additionally, batching vector database injections (e.g., in groups of 20) minimizes the overhead of individual API/IPC calls.
**Action:** Always prefer `split(None, maxsplit)` for truncation and implement batching for database-intensive operations.
