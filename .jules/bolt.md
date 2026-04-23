## 2025-05-15 - [Character-count heuristic for word limit pre-filtering]
**Learning:** Using a character length threshold (e.g., 150,000 chars) as a pre-filter before performing expensive `split()` operations to check word limits significantly reduces CPU overhead for standard-sized documents.
**Action:** Always use string length checks as a low-cost heuristic before running complex regex or string segmentation on large text corpora.
