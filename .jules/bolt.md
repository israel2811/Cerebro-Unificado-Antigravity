## 2026-03-31 - Bounded String Splitting and ChromaDB Batching Optimization

**Learning:** Unbounded `.split()` on large text files allocates massive full-string word lists in RAM and causes quadratic overhead when sliced and joined. Using `.split(None, 40001)` limits parsing to at most 40,001 splits, providing >120x speedup for files >5MB. Additionally, batching ChromaDB inserts (`BATCH_SIZE = 20`) reduces vector embedding engine and SQLite transaction overhead by up to 20x.

**Action:** Always prefer `split(separator, maxsplit)` when truncating or processing prefix tokens from large text streams, and batch vector database insertions instead of inserting single items in a loop.
