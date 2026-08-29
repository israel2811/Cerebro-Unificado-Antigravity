## 2026-03-30 - Maxsplit Optimization for String Word Truncation

**Learning:** Unbounded `.split()` on large text files (1MB+ / 100k+ words) creates an unnecessary full list of all word substrings in memory. When truncating string length by word count (e.g., to 40,000 words for embedding batch limits), passing `maxsplit=40001` to `split(None, 40001)` stops splitting after the limit is reached, achieving a ~37x speedup and significantly reducing memory allocations.

**Action:** Always specify `maxsplit` when splitting large string contents if only the first $N$ tokens/words are needed for processing or truncation.
