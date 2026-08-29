## 2025-04-26 - ChromaDB Batch Indexing and 'Batch Poisoning'
**Learning:** When implementing batch processing for vector databases, failing to reset the batch state in a `finally` block after an error leads to 'poisoned batches'. Subsequent valid items are appended to the failing batch, causing cascading failures. Also, character-length heuristics are significantly cheaper than `.split()` for pre-filtering large documents.
**Action:** Always use `try...finally` to reset batch state in accumulation loops. Use `len(string)` pre-filters before expensive string operations.
