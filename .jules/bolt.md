# Bolt's Performance Journal

## 2026-05-26 - Truncation and Batching in ChromaDB
**Learning:** Using `.split()` without arguments on large strings repeatedly is expensive. `split(None, maxsplit)` is much more efficient for checking word limits or truncating. Also, ChromaDB's `collection.add()` is significantly faster when used with batches instead of individual items.
**Action:** Always use `maxsplit` when only a subset of words is needed, and prefer batch operations for database insertions.
