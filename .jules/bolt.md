## 2026-06-11 - Optimized Truncation with `split(None, N)`
**Learning:** In Python, `string.split()` without arguments splits the entire string, which is $O(\text{length of string})$ and memory intensive for large files. Using `split(None, N+1)` with `maxsplit` is significantly faster (~100x for 1M words) because it stops processing after $N+1$ fragments are found.
**Action:** Always use `maxsplit` when checking for word-count limits or truncating long strings by word count.

## 2026-06-11 - ChromaDB Batching Efficiency
**Learning:** ChromaDB (and similar vector DBs) incur significant transaction and I/O overhead for each `collection.add()` call. Batching documents (e.g., in groups of 20-100) reduces this overhead and allows for parallelized embedding generation by the underlying model.
**Action:** Implement batching for vector database injections, ensuring a `finally` block or helper function clears the batch state to prevent 'poisoned batches' in case of partial failures.
