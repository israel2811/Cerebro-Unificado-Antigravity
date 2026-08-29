## 2026-05-20 - Use `maxsplit` for Word-Count Truncation in Large Text

**Learning:** Using `str.split()` on large strings (e.g., 10MB+) in Python is extremely expensive as it creates a full list of all words in memory. When you only need to check if a word count exceeds a threshold or need to truncate to a specific count, `str.split(None, maxsplit)` is significantly faster (~200x speedup in benchmarks) because it stops processing the string as soon as the limit is reached.

**Action:** Always use `maxsplit` when truncating or checking word counts in large text buffers. Combine with a character-length heuristic (e.g., `len(text) > threshold`) as a cheap pre-filter to avoid any splitting when the condition is obviously not met.

## 2026-05-20 - Batching Database Operations with State Safety

**Learning:** Batching multiple items into a single database call (like `collection.add` in ChromaDB) significantly reduces IPC overhead and indexing time. However, it's critical to clear the batch lists in a `finally` block if an error occurs during the batch operation to prevent "poisoned batches" from affecting subsequent operations.

**Action:** Implement batching for all bulk database insertions. Always wrap the batch flush in a try-finally block to ensure the batch state is reset regardless of success or failure.
