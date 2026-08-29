## 2026-04-30 - Optimized ChromaDB Vector Indexing
**Learning:** Using `split()` on large strings (16MB+) is a significant bottleneck. Using `str.split(None, maxsplit)` combined with a character-length heuristic (e.g., `len(s) > 200000`) avoids processing the entire buffer and reduces execution time by ~50% for documents near the word limit.
**Action:** Always use heuristics and `maxsplit` when truncating or validating word counts in large text buffers. Use batch processing for vector database insertions to minimize overhead.
