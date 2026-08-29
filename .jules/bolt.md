## 2026-06-21 - Batching and Truncation in RAG Pipelines
**Learning:** Individual `collection.add()` calls in ChromaDB are significantly slower than batched calls due to overhead per transaction. Furthermore, using `split()` on large strings without `maxsplit` causes unnecessary memory allocation and processing time.
**Action:** Always implement batching (e.g., size 20) for vector database injections and use `string.split(None, N)` when truncating to the first N words to optimize performance and reduce memory spikes.
