# BOLT'S JOURNAL - PERFORMANCE OPTIMIZATIONS

## 2026-06-12 - Optimized RAG Indexer with Batching and Efficient Truncation
**Learning:** In ChromaDB (and similar vector DBs), individual `collection.add` calls for single documents create significant overhead. Consolidating into batches (e.g., 20) improves throughput dramatically. Also, using `split(None, N)` with `maxsplit` is significantly faster (~140x) for truncation than full string splitting for large documents.
**Action:** Always batch vector DB writes and use `maxsplit` when truncating large strings in Python.
