# Bolt's Journal - Critical Learnings

## 2026-02-17 - Maxsplit and Batching Optimization in ChromaDB Indexing
**Learning:** Calling `split()` without arguments on large corpus texts splits the entire string in memory. When checking length and slicing, doing `len(contenido.split())` and `contenido.split()[:40000]` performs full string splits twice. Using `split(None, 40001)` limits the split iterations and memory overhead. Additionally, batching ChromaDB inserts (`collection.add`) in batches of 20 avoids per-document SQLite transaction and model forward pass overhead.
**Action:** Always use `split(None, maxsplit)` when truncating large string inputs and batch database insertions to optimize throughput.
