## 2026-03-01 - Batching Vector Database Insertions in ChromaDB
**Learning:** Calling `collection.add()` individually per document causes significant I/O and transaction overhead in ChromaDB. Grouping document insertions into batches (e.g. `BATCH_SIZE = 20`) reduces database transaction lock and index commit calls up to 20x.
**Action:** Always batch vector database insertions (`collection.add`) when indexing corpus chunks, ensuring residual buffers are flushed after loop completion.
