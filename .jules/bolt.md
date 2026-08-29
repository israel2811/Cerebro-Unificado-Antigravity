## 2026-06-29 - Efficient String Truncation
**Learning:** Using `string.split(None, N)` is significantly faster than `string.split()[:N]` for large strings because it avoids creating a full list of words in memory when only a subset is needed.
**Action:** Always use `maxsplit` parameter when truncating text by word count.

## 2026-06-29 - Vector DB Batching
**Learning:** Individual calls to `collection.add()` in ChromaDB (and other vector databases) incur high overhead per operation. Batching multiple documents into a single call reduces total time linearly with batch size.
**Action:** Implement batching (e.g., size 20-100) for all vector database ingestion tasks.
