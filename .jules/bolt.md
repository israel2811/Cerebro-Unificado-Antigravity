## 2026-07-27 - Optimized Word-Count Truncation in RAG Indexer
**Learning:** Double calling `.split()` on very large text blocks (O(N) operations) inside loop processing results in massive CPU and memory footprint. Python's `split(None, maxsplit)` parameters can be leveraged to halt splitting early when the maximum required chunks have been met, preventing complete string scanning.
**Action:** Replace multiple `.split()` with `split(None, 40000)` and measure performance to ensure > 30x faster chunking.
