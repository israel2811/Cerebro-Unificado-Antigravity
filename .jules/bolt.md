## 2026-06-11 - Optimized ChromaDB Ingestion
**Learning:** For vector database ingestion (ChromaDB), individual `collection.add()` calls create significant overhead. Batching documents (e.g., size 20) drastically reduces total processing time. Additionally, using `split(None, N+1)` for truncation is significantly faster than a full `.split()[:N]` as it avoids full-string processing and massive list creation.
**Action:** Always prefer batching for I/O bound operations like vector DB adds. Use `maxsplit` parameter in `split()` when only a prefix of words is needed.
