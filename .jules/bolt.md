## 2026-06-12 - [Initial Research]
**Learning:** Found that `04_chromadb_rag_indexer.py` performs individual `collection.add` calls for each file and uses inefficient `split()` for truncation.
**Action:** Implement batching and optimized string splitting to improve indexing performance.
## 2026-06-12 - [Batching Optimization]
**Learning:** Batching `collection.add` calls significantly reduces overhead compared to individual additions. In environments without `chromadb` installed, mocking `sys.modules` allows for robust logic verification.
**Action:** Use batch size of 20 as a safe default for local ChromaDB instances to balance memory and speed.
