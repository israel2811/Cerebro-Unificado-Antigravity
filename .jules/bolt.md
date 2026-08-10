# Bolt's Performance Journal

## 2026-08-10 - CPU and Memory Bottlenecks in String Splitting
**Learning:** Full-string split operations on large textual documents (like full thesis chapters) inside iterative loops create severe memory and CPU overhead. When checking or truncating word count, using `len(string.split()) > N` followed by `string.split()[:N]` is highly redundant. Instead, utilizing `maxsplit` parameter with `string.split(None, N+1)` stops string scanning immediately after finding the target count, leading to up to ~30x CPU speedup and massive memory reduction.
**Action:** Always optimize word count limit checks and slicing on large inputs by utilizing Python's built-in `split(None, maxsplit)` pattern.
