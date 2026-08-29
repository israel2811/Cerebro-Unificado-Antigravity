## 2026-06-12 - Optimized Word Truncation and Batching in ChromaDB Indexer

**Learning:** Using `string.split()` without arguments twice on large documents (e.g., 17MB) causes redundant full-string scans and massive memory allocation. Python's `split(None, N)` with `maxsplit` is significantly faster for truncation. Also, single-document insertion in ChromaDB is a bottleneck due to repeated transaction overhead.

**Action:** Replace `len(s.split()) > N` with `s.split(None, N+1)` and use batch processing (e.g., `BATCH_SIZE = 20`) for vector database injections to minimize overhead and improve throughput.
