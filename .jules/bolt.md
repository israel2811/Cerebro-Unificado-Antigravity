## 2026-03-02 - Python String Split `maxsplit` Truncation Optimization

**Learning:** When checking or truncating large string contents by word count (e.g. `len(text.split()) > N`), calling plain `text.split()` without `maxsplit` parses the entire string into memory and creates an array of all words across the entire document. For multi-megabyte strings, passing `maxsplit=N+1` (`text.split(None, N+1)`) stops tokenizing as soon as `N+1` elements are produced, yielding speedups from ~25x (1MB text) to >200x (10MB+ text) while drastically reducing short-lived heap allocations.

**Action:** Always use `str.split(None, N + 1)` when checking if a string exceeds `N` words or when taking the first `N` words of a large text buffer.
