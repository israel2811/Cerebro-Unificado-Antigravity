## 2026-06-11 - Optimizing ChromaDB Indexing Performance

**Learning:** Individual calls to `collection.add` in ChromaDB create significant overhead. Batching these calls reduces the number of roundtrips and leverages internal optimizations. Additionally, using `split(None, maxsplit)` is significantly more efficient than full string splitting for truncation.

**Action:** Implement batching (BATCH_SIZE=20) and optimized word truncation in `scripts_leviathan/04_chromadb_rag_indexer.py`.
