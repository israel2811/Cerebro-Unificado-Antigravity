## 2026-03-30 - Maxsplit Optimization vs Full Splitting in Large Text Files
**Learning:** Calling `.split()` without `maxsplit` on multi-megabyte string inputs causes complete string parsing and full list allocation in memory. Using `.split(None, 40001)` stops tokenization after reaching the target limit, yielding ~240x speedups (from ~1312ms down to ~5.4ms on 10MB text strings).
**Action:** Always specify `maxsplit` when tokenizing or truncating strings with a target word limit.
