## 2026-05-12 - Batch processing and string optimization in ChromaDB indexer
**Learning:** Individual document insertions into ChromaDB cause significant overhead due to repeated database calls and embedding generation triggers. Additionally, using `len(s.split())` on large strings in a loop is an O(N) operation that can be avoided with character-length heuristics and `maxsplit`.
**Action:** Implement batching (e.g., BATCH_SIZE=50) for database insertions and use `split(None, maxsplit)` to optimize string truncation.
