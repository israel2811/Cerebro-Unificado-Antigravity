## 2026-05-31 - Maxsplit for Word Count Truncation
**Learning:** Using `text.split()` without arguments on large strings (e.g., 17MB+ corpus) to check word counts or truncate is extremely inefficient as it creates a full list of all words in memory twice. Using `text.split(None, N+1)` with `maxsplit` is significantly faster (~100x for 1M words) and more memory-efficient.
**Action:** Always use `maxsplit` when truncating or checking word counts in large text buffers.

## 2026-05-31 - Robust Batch Processing in RAG
**Learning:** Moving from individual database calls to batch calls (e.g., in ChromaDB) provides a massive performance boost (~10x) but requires careful error handling. A single `try-except` around the whole loop is a regression; instead, use a helper function to flush batches and maintain granular error handling for file IO to skip bad files without crashing the enitre process.
**Action:** Use a `flush_batch` helper and nested `try-except` blocks when implementing batch processing for document indexing.
