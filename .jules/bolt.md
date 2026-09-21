# Bolt's Performance Journal

## 2026-03-30 - Python `str.split(sep, maxsplit)` vs Unbounded Double `.split()`

**Learning:** Calling `.split()` without a `maxsplit` parameter on large strings (e.g., multi-megabyte corpus documents) causes Python to allocate memory and create string objects for every single word in the entire document. When combined with checking `len(str.split())` before slicing `str.split()[:N]`, this performs two full unbounded string splits over the entire corpus. Utilizing `maxsplit` (e.g., `words = text.split(None, 40001)`) limits allocation to N+1 elements, yielding a ~45x to >200x performance speedup on large text inputs while drastically reducing memory churn.

**Action:** Whenever truncating or checking word bounds on potentially large text inputs, always use `str.split(sep, maxsplit)` to bound the split operation.
