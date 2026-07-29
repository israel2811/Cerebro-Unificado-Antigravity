## 2026-07-29 - [Optimizing Word-Count Truncation in Text-Processing Pipelines]
**Learning:** Performing standard full-string `.split()` operations multiple times on large (100k+ words) text files is a major CPU and memory allocation bottleneck. Utilizing `.split(None, maxsplit)` where possible avoids fully parsing and allocating lists for the remainder of the text when only a prefix slice is needed.
**Action:** Always use `.split(None, maxsplit)` to perform partial word-count truncation or slicing in Python instead of full splitting followed by slice operations.
