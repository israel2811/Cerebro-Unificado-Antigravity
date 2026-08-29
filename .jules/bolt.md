## 2026-05-30 - Efficient word-count truncation in Python
**Learning:** Using `text.split()` without arguments on large strings creates a full copy of all words in memory, which is $O(N)$ in time and space. When only checking for a limit or truncating, `text.split(None, maxsplit=N+1)` is significantly faster as it stops as soon as it finds $N+1$ words, and the space overhead is limited to the result list of size $N+1$. In my benchmarks, this was ~120x faster for 1M words.
**Action:** Always use `maxsplit` when truncating or checking word counts in large text buffers.

## 2026-05-30 - Batch processing in ChromaDB
**Learning:** ChromaDB's `collection.add` has significant per-call overhead (likely due to internal SQLite transactions and embedding model initiations). Batching multiple documents into a single call significantly improves throughput.
**Action:** Implement batching with a reasonable size (e.g., 50-100) for all vector database ingestion tasks.

## 2026-05-30 - Avoiding "Batch Poisoning"
**Learning:** When using a `try...except` loop for batching, if the batch operation fails, the state (accumulated lists) must be explicitly reset in a `finally` block. Otherwise, subsequent valid items will keep being added to a "poisoned" batch that continues to fail, leading to cascading errors.
**Action:** Always clear batch buffers in a `finally` block after an attempted flush.
