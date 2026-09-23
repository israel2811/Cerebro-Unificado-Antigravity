# Bolt Performance Journal

## 2026-08-30 - Truncating Large Strings with split(None, N)
**Learning:** Calling `text.split()` on large text files without `maxsplit` parses and creates a Python list for every single word in memory, even if we only need the first N words. Using `text.split(None, maxsplit + 1)` stops splitting after the limit, achieving ~100x speedup and drastically lower memory allocation.
**Action:** Always use `split(None, maxsplit)` when checking or slicing word counts up to a fixed limit on large strings.
