# Bolt's Performance Journal ⚡

## 2026-05-17 - [Optimizing String Truncation in Python]
**Learning:** Using `text.split()` on large strings (e.g., 15MB+) to count words or truncate is extremely slow because it allocates a list for every single word in the buffer. For a 40,000 word limit, using `text.split(None, 40001)` is ~260x faster as it stops processing once the limit is reached. Additionally, a character-length heuristic (`len(text) < limit`) can skip the split entirely for smaller strings.
**Action:** Always use `maxsplit` when truncating or checking word counts in large text buffers.
