# Bolt's Journal - Critical Learnings

## 2026-02-17 - Word-count Truncation Optimization
**Learning:** `split(None, N)` using `maxsplit` avoids creating huge list allocations in Python when only taking a prefix of words.
**Action:** Use `maxsplit` parameter in `.split()` when truncating text by word count.
