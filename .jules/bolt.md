
## 2026-06-21 - [ChromaDB Indexer Optimization]
**Learning:** Batching `collection.add` calls significantly reduces the overhead of vector database ingestion. Additionally, using `split(None, N+1)` is much more efficient than multiple full-string `split()` calls for large text files.
**Action:** Always implement batching for vector ingestion and use `maxsplit` in string operations when dealing with large corpora to avoid memory spikes and redundant processing.
