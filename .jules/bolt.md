# Bolt's Performance Journal - Critical Learnings Only

## 2026-07-26 - [ChromaDB Indexer Truncation Maxsplit Optimization]
**Learning:** Full-string `.split()` calls on massive strings are extremely slow and CPU/memory-intensive because they allocate and return arrays for all elements. By passing a `maxsplit` parameter (e.g., `split(None, 40000)`), Python ceases tokenization as soon as the limit is hit, avoiding needless parsing and reducing CPU and memory overhead dramatically.
**Action:** Always prefer `split(None, max_limit)` over `split()[:max_limit]` when checking or truncating string tokens up to a specific limit in large input streams.
