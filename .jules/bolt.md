## 2026-05-18 - Optimized String Truncation and ChromaDB Batching

**Learning:** Using `len(text.split())` for word-count-based truncation is a major performance bottleneck for large text files (>10MB), as it creates a full list of words in memory. This is especially risky in memory-constrained environments like our 2GB RAM VM. Additionally, single-document insertions in ChromaDB incur significant overhead compared to batching.

**Action:** Always use a character-length heuristic (`len(text) > threshold`) as a pre-filter before splitting, and use `split(None, maxsplit)` to avoid processing the entire buffer beyond what is needed. Implement batching for database operations (e.g., BATCH_SIZE=50) to minimize IPC/network overhead.
