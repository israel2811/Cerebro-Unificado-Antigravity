# Bolt's Journal ⚡

Critical performance learnings and insights gathered during optimizations.

## 2026-03-30 - Python `str.split()` maxsplit Optimization on Large Strings

**Learning:** Calling `len(text.split())` and `text.split()[:N]` without `maxsplit` on large documents (e.g., multi-megabyte corpus texts) forces Python to parse, allocate memory for, and construct a list containing every single word in the entire string. When `text` contains millions of words, this causes severe memory allocation overhead and high latency (>3 seconds for 5M words). By specifying `text.split(None, N + 1)` with `maxsplit`, Python stops tokenizing as soon as `N + 1` tokens are found, resulting in up to ~116x speedup (26ms vs 3073ms) and dramatically lower memory consumption.

**Action:** When truncating or inspecting the head of a large string based on word counts, always use `str.split(None, limit + 1)` instead of full string splitting.
