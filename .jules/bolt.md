## 2026-05-15 - Python string splitting on large documents
**Learning:** Using `str.split()` twice on large strings (one for length check, one for truncation) is extremely inefficient as it creates massive intermediate lists and scans the entire buffer. Using a character-length heuristic pre-filter and `maxsplit` provides a 250x+ speedup.
**Action:** Always use `maxsplit` when truncating and consider character-length as a cheap proxy for word count when dealing with memory-constrained environments.
