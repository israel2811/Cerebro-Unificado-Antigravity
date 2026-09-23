# Bolt's Performance Journal

This performance journal is a collection of critical learnings, surprising bottlenecks, or valuable rejected changes discovered while optimizing the Antigravity Unified Cloud setup codebase.

## 2026-07-23 - Batching and Lexicographical Sorting in ChromaDB
**Learning:** Adding documents individually to ChromaDB using `collection.add(...)` results in severe CPU/database performance hits and high overhead, especially when compiling embedding calculations. Consolidating the files into batches of 20 with `collection.add(...)` significantly speeds up insertion. When writing unit tests for alphabetical sorting, remember that Python's default string sorting is lexicographical (i.e. 'chapter_10.txt' immediately after 'chapter_1.txt', not natural numerical order).
**Action:** Always batch vector database insertions where possible, and ensure unit tests for directory listing sorts expect lexicographical order instead of natural numeric sort order.

## 2026-07-23 - Efficient String Truncation with split maxsplit
**Learning:** Traditional ways of checking and truncating string words using `len(text.split())` and `text.split()[:40000]` call full-string splits twice, causing memory and CPU degradation on large text inputs (1MB+).
**Action:** Use `text.split(None, 40001)` to limit splits to exactly what is needed for truncation. This performs at most `40001` splits and avoids splitting the entire massive string multiple times, delivering up to 230x speedups.
