## 2026-06-13 - [ChromaDB Indexing & Python Truncation]
**Learning:** String truncation using 'split()[:N]' is O(N) in memory and time. Using 'split(None, N+1)' is O(N_words) up to N, significantly reducing overhead for large files. Batching collection.add() calls in ChromaDB (batch size 20) reduces indexing overhead by an order of magnitude.
**Action:** Always use 'maxsplit' when truncating strings by word count. Implement batching for vector database injections to avoid N+1 overhead.
