## 2026-06-03 - Efficient word-count truncation in Python
**Learning:** Using `text.split()` on large strings (like 17MB+ corpus files) to check word counts or truncate is expensive because it creates a full list of all words in memory. `text.split(None, maxsplit)` is significantly faster and more memory-efficient as it stops splitting after `maxsplit` is reached.
**Action:** Always use `maxsplit` when truncating or checking word counts in large text buffers.

## 2026-06-03 - Batched ChromaDB Indexing
**Learning:** Individual `collection.add` calls in ChromaDB are slow due to transaction overhead and sequential embedding generation. Batching documents (e.g., size 20) improves throughput by ~10x in simulated environments by consolidating transactions and allowing the embedding model to process multiple inputs at once.
**Action:** Implement batching for all vector database injection scripts. Ensure batch state is cleared in a `finally` block to prevent "batch poisoning" on errors.
