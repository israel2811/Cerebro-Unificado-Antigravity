# Bolt Performance Journal

## 2026-05-02 - Initial Assessment
**Learning:** Found multiple memory bottlenecks in the Leviathan data pipeline, specifically in `02_docs_prep_injector.py` (eager file reading and massive list creation via `.split()`) and `04_chromadb_rag_indexer.py` (lack of batching for database insertions).
**Action:** Focus on implementing batch processing in `04_chromadb_rag_indexer.py` to reduce database IPC overhead and improve throughput, as this is a high-impact "low hanging fruit" optimization.
