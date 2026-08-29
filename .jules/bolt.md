## 2026-06-25 - ChromaDB Indexing Optimization
**Learning:** Documented significant performance bottlenecks in individual document indexing and string manipulation. Batching documents for ChromaDB reduces API call overhead by ~20x (batch size 20). Using `split(None, maxsplit)` for truncation avoids full-string splitting, providing up to 60x speedup for 10MB strings compared to standard `.split()[:limit]`.
**Action:** Always batch vector database injections and use `maxsplit` when truncating large strings by word count to minimize memory and CPU overhead.
