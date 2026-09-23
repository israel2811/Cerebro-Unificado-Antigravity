# Bolt's Performance Journal ⚡

Welcome to Bolt's Performance Journal. This journal tracks only critical performance learnings, surprising bottlenecks, failed optimizations, or valuable rejected changes.

## 2026-06-21 - RAG Indexer Word Splitting Optimization
**Learning:** Calling `.split()` on large corpus text strings (e.g., 200k+ words) without a limit performs a full split on the entire string, which consumes substantial CPU cycles and RAM. When we only need the first 40,000 words, calling `.split(None, 40001)` stops splitting after the limit, resulting in up to 20x speedup and significantly lower peak memory usage. Also, avoiding duplicate `.split()` calls by caching the result prevents redundant computations.
**Action:** When truncating strings or processing text sequences by word boundaries where only a prefix is needed, always specify a `maxsplit` parameter in `split()` to avoid full-string processing. Caching split results or keeping word counts in variables prevents repeating $O(N)$ split operations.
