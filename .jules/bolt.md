## 2026-05-15 - Python String Splitting Performance
**Learning:** Using `.split()` on large text buffers creates a full list of all words in memory, which is O(n) in both time and space. When only a subset of words is needed (e.g., for truncation or word count checks), `split(None, maxsplit)` is significantly more efficient as it stops splitting after `maxsplit` is reached.
**Action:** Always use `maxsplit` with `split()` when checking for word count limits or truncating large strings.
