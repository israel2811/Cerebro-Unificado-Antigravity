## 2026-06-02 - Python split() Performance in Large Buffers
**Learning:** Calling `.split()` on a multi-megabyte string multiple times (e.g., for counting and then for slicing) causes redundant memory allocations and CPU overhead. Using `split(None, N+1)` (maxsplit) allows for O(N) word counting and prefix extraction without processing the entire buffer.
**Action:** Always use `maxsplit` when you only need to check if a word limit is exceeded or when you only need the first N words of a large text.
