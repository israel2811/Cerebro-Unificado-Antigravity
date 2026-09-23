## 2026-03-30 - ChromaDB Indexer Word Truncation & Batching
**Learning:** Calling `split()` twice on multi-megabyte strings creates huge full-string word lists and takes 0.77s vs 0.004s when using `split(None, 40001)`. Additionally, batching ChromaDB inserts in chunks of 20 vectorizes embedding inference and drastically reduces ChromaDB transaction overhead.
**Action:** Use `split(None, maxsplit)` for length-based string truncation and batch database inserts in vector DB pipelines.
