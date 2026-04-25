## 2025-04-25 - ChromaDB Indexing Bottlenecks
**Learning:** O(N) database insertions for vector databases (ChromaDB) introduce significant IPC and network overhead. Additionally, expensive string operations like `.split()` on large documents can be avoided using simple length-based heuristics.
**Action:** Use batching (BATCH_SIZE = 50) for `collection.add()` and implement a character-count pre-filter (200k chars ~ 40k words) before performing word-count checks.
