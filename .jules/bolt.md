## 2026-07-02 - Optimized ChromaDB Indexing with Batching and Efficient Truncation

**Learning:** Individual `collection.add` calls for each document in ChromaDB introduce significant overhead, especially when using remote or persistent storage. Additionally, using `split()` twice on potentially large strings for truncation is a memory and CPU anti-pattern.

**Action:** Implement batch processing (e.g., `BATCH_SIZE = 20`) to consolidate API calls and use `split(None, maxsplit)` to efficiently truncate large documents without processing the entire string twice.
