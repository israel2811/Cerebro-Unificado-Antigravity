# ⚡ Bolt Performance Journal

## 2026-05-11 - String Truncation Bottleneck in Python
**Learning:** Using `len(str.split())` to count words on large strings (e.g., >10MB) is extremely slow because it creates a massive intermediate list of strings. `str.split(None, maxsplit)` is significantly faster as it stops after reaching the limit. Additionally, using `len(str)` as a pre-filter heuristic (char count >= word count) avoids splitting entirely for small strings.
**Action:** Always use `split(None, N)` when only the first N words are needed, and use character length heuristics to skip expensive operations.
