# Bolt Performance Journal

## 2025-04-23 - Memory-Efficient Processing Patterns
**Learning:** The execution environment has a strict 2GB RAM limit. Large text files (like `raw_corpus_extraction.txt`) can easily cause OOM if loaded entirely into memory.
**Action:** Use generator-based streaming for large file processing and implement character-length heuristics to avoid expensive string operations like `.split()` on large buffers unless necessary.

## 2025-04-23 - ChromaDB Batch Indexing
**Learning:** ChromaDB performance is significantly improved by batching `collection.add()` calls rather than adding documents individually. This reduces IPC/network overhead and allows for vectorized embedding calculations.
**Action:** Implement a `BATCH_SIZE` (e.g., 50) and ensure robust error handling with `try-except-finally` to prevent batch poisoning.
