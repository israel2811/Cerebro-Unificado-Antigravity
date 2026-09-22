## 2026-02-18 - Avoid full string splitting when capping word count

**Learning:** Using `len(s.split())` followed by `" ".join(s.split()[:N])` splits large strings (e.g. multi-megabyte corpus files) into complete lists twice, allocating memory for every single word in the document even when only the first N words are needed. Utilizing `s.split(None, N)` stops splitting as soon as N+1 chunks are parsed, yielding an 18x to 140x speedup and significantly reducing temporary memory allocations.

**Action:** When truncating or inspecting leading words from large text streams, pass `maxsplit` to `.split()` or stream the inputs rather than parsing the full string.
