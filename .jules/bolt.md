# ⚡ Bolt's Performance Journal - Leviathan Project

## 2026-04-30 - ChromaDB Batch Indexing Bottleneck
**Learning:** Sequential calls to `collection.add()` for individual documents in `04_chromadb_rag_indexer.py` incur significant network/IPC overhead and miss out on vectorized embedding opportunities. In a constrained 2GB RAM environment, this inefficiency slows down the indexing of the 17MB corpus significantly.
**Action:** Always implement batch processing (e.g., BATCH_SIZE=50) for vector database insertions to optimize throughput. Use character-length heuristics as a pre-filter for expensive string operations like `.split()` to further reduce CPU load.
