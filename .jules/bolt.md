## 2026-07-16 - Efficient String Truncation in Python
**Learning:** Using `.split()` without arguments on a large string to check word count followed by another `.split()[:N]` is O(N) but with a large constant factor because it allocates a full list of all words twice. Using `.split(None, N+1)` (maxsplit) avoids splitting the entire string if only the first N words are needed.
**Action:** Always use `maxsplit` when truncating strings by word count to save memory and CPU.

## 2026-07-16 - ChromaDB Batching
**Learning:** Individual `collection.add()` calls in ChromaDB (and most vector DBs) have significant overhead. Batching documents (e.g., size 20-100) significantly improves throughput.
**Action:** Implement batching for all vector database ingestion tasks.
