# Bolt Journal ⚡

## 2026-03-01 - Avoid full-string split on large inputs via `maxsplit` parameter
**Learning:** Calling `len(text.split())` on large text corpus files (e.g. 10MB strings) creates an intermediate list of all split words (~1.5 million strings), causing heavy allocation overhead (~1000ms). Setting `maxsplit=40001` with `text.split(None, 40001)` stops splitting after 40,001 items, reducing processing time down to ~5ms (>200x speedup).
**Action:** Always pass `maxsplit` when checking length or truncating large string inputs in Python when only a bounded prefix of tokens is needed.
