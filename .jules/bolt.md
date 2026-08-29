## 2026-05-14 - Expensive String Splitting in Large Document Processing
**Learning:** Using `str.split()` on large text buffers (e.g., 10MB+) creates massive in-memory lists, consuming significant CPU and RAM. In scenarios like ChromaDB truncation where only a word count limit is needed, a character-length heuristic (`len(s) > limit`) followed by `split(None, limit + 1)` avoids processing the entire buffer.
**Action:** Always use `maxsplit` and a fast character-count pre-filter when truncating or validating large strings to avoid O(N) overhead where N is the full string size.
