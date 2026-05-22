## 2026-05-22 - Optimized word-count truncation with maxsplit
**Learning:** Using `split()` on large strings (e.g., >10MB) creates massive in-memory word lists, leading to high CPU and RAM usage. Python's `split(None, N)` with the `maxsplit` parameter allows stopping the split operation early once the required number of words is found.
**Action:** Always use `maxsplit` when checking if a string exceeds a word count threshold or when truncating to a specific word count. Avoid double `split()` calls by reusing the result of a single `maxsplit` call.
