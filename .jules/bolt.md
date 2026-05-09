# Bolt's Performance Journal ⚡

## 2026-05-07 - Inefficient processing in 04_chromadb_rag_indexer.py
**Learning:** The script `04_chromadb_rag_indexer.py` contains a classic performance anti-pattern: it performs a full `split()` twice on potentially large documents to check and then truncate word count. Additionally, it inserts documents one-by-one into ChromaDB, which incurs high overhead due to repeated database IPC and indexing triggers. Using `split(None, maxsplit)` with a character-length heuristic can provide a >100x speedup for truncation, and batching `collection.add()` calls significantly reduces database overhead.
**Action:** Replace redundant `split()` calls with optimized truncation and implement batching for database insertions.
