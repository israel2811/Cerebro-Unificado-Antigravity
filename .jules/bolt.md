## 2025-04-07 - Optimized ChromaDB Vector Indexing
**Learning:** In resource-constrained environments (2GB RAM), batching vector database insertions significantly reduces overhead. Additionally, using string length as a pre-filter before expensive operations like `.split()` or `.join()` on large text files saves measurable CPU cycles and memory by avoiding unnecessary object creation for smaller files.
**Action:** Always implement batching (e.g., BATCH_SIZE=50) for vector database indexing and use character-count pre-filters before word-count checks on large text documents.

## 2025-04-07 - Robust Batch Processing in Leviathan
**Learning:** When implementing batch processing in data pipelines, it is critical to ensure that batch state is reset regardless of whether an individual batch operation succeeds or fails. Failure to reset batch state (e.g., within a `finally` block) can lead to infinite retry loops of failing data, potentially halting the entire pipeline.
**Action:** Robust batch processing requires nested error handling: wrap individual file operations and batch-add operations in separate try-except blocks to ensure the process continues if a single item or batch fails. Always include a 'flush' step after loops.
