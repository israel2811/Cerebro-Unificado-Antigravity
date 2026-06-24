## 2026-06-24 - Efficient Word Truncation and Batching in ChromaDB Indexer

**Learning:** Using `string.split()[:N]` on very large strings is inefficient because it creates a full list of all words before slicing. `string.split(None, N)` (using `maxsplit`) is significantly faster as it stops splitting once the limit is reached. In this codebase, it provided a ~34x speedup on a 1M word string. Also, single-document insertions in ChromaDB are much slower than batched insertions due to overhead per call.

**Action:** Always use `maxsplit` when truncating strings by word count. Implement batching for vector database insertions (standard size 20-100) to reduce network/IPC overhead.
