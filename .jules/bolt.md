## 2026-05-10 - Performance Heuristics & Batching in ChromaDB
**Learning:** For text processing pipelines in memory-constrained environments (2GB RAM), full string operations like `.split()` on large documents (15MB+) are extremely expensive (1.5s+). Implementing a character-length heuristic pre-filter and using `split(None, maxsplit)` can yield a 10x speedup for large files and 400x for small ones.
**Action:** Always use `len()` as a cheap pre-filter for string processing and prefer `maxsplit` parameters when truncating or partially parsing large buffers.
