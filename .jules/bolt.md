## 2025-05-15 - Efficient String Truncation and Batching in ChromaDB Indexer
**Learning:** Using `string.split()` without `maxsplit` on large documents is a performance bottleneck as it tokenizes the entire string even if only a small prefix is needed. Additionally, sequential `collection.add()` calls in ChromaDB (or any vector DB) introduce significant overhead compared to batching.
**Action:** Always use `split(None, N+1)` when checking if a string exceeds N words. Implement batching for vector database insertions to reduce IO/API overhead.

## 2025-05-15 - Testing Batching with State Reset
**Learning:** When testing functions that manage state in a `finally` block (like clearing a batch list), standard mock call inspection (`call_args_list`) may report empty lists because the reference held by the mock points to the now-cleared list.
**Action:** Use a `side_effect` in the mock to capture a deep copy (e.g., `list(kwargs['documents'])`) of the arguments at the time of the call.
