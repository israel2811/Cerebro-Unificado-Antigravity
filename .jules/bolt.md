# Bolt Performance Journal ⚡

## 2026-03-30 - Optimize String Truncation with maxsplit Parameter
**Learning:** Using `str.split()` without arguments on multi-megabyte text files causes Python to scan the entire string and build a list containing every word in memory. When performing word-count checks or truncation (e.g. capping chunks at 40,000 words), passing `maxsplit=40001` (`str.split(None, 40001)`) stops string splitting immediately after reaching the target word count threshold. This provides up to a ~100x speedup and saves significant RAM allocation overhead on large input files.
**Action:** When validating or truncating word counts on large text strings, always use `str.split(None, target_limit + 1)` rather than splitting the full string.
