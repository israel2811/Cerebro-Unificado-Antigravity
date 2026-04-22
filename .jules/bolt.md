# Bolt Performance Journal

## 2025-04-22 - Batch Indexing and Heuristic Pre-filtering in ChromaDB
**Learning:** For vector database indexing (ChromaDB), single-item insertions incur significant overhead due to repeated network/IPC calls and lack of vectorized embedding operations. Additionally, performing high-frequency string operations like `.split()` on large texts can be a CPU bottleneck.
**Action:** Use batching (e.g., BATCH_SIZE = 50) for database insertions. Implement character-length heuristics (e.g., `len(text) > threshold`) as a fast pre-filter before executing expensive semantic checks or transformations.

## 2025-04-22 - Robust Batch Processing Error Handling
**Learning:** Failing to reset the batch state (clearing lists) in a `finally` block after an error leads to 'poisoned batches' where subsequent valid items are appended to a failing batch, causing cascading failures.
**Action:** Always wrap batch-add operations in a `try-except-finally` block to ensure the batch is flushed or cleared, regardless of success or failure.

## 2025-04-22 - Memory-Efficient Streaming for Large Corpus Processing
**Learning:** Loading a large concatenated corpus (e.g., 17MB+ `raw_corpus_extraction.txt`) entirely into memory for cleaning and chunking can lead to Out-Of-Memory (OOM) errors in RAM-constrained environments (2GB limit).
**Action:** Transition from bulk `f.read()` to generator-based streaming or document-by-document processing to keep peak memory usage within safe limits.
