## 2026-06-15 - [ChromaDB Indexing Optimization]
**Learning:** Batching `collection.add` calls in ChromaDB significantly reduces overhead from embedding generation and IPC/Network latency. Also, using `split(None, maxsplit)` for string truncation is orders of magnitude faster than full `split()` followed by slicing on large documents.
**Action:** Always implement batching (e.g., BATCH_SIZE=20) for vector database insertions and use `maxsplit` when checking for word limits in large text blocks.

## 2026-06-15 - [Micro-optimization vs Readability]
**Learning:** Changing a stable function's return signature (e.g., from `List[str]` to `List[Tuple[str, int]]`) to avoid a single redundant `split()` in a logging statement is a "micro-optimization" that sacrifices code readability and introduces breaking changes.
**Action:** Prioritize API stability and readability over negligible performance gains. Only refactor core signatures if the performance bottleneck is significant and measurable in a hot path.
