# Bolt's Performance Journal

## 2026-06-15 - Catastrophic Backtracking with Regex over Large Text Corpus files
**Learning:** Using regular expressions like `re.sub(r'\{.*?\}', '', text, flags=re.DOTALL)` to strip out JSON objects or nested curly-braced noise from multi-megabyte corpus texts (e.g., 16MB+) is highly expensive and prone to catastrophic backtracking or huge engine execution times due to the non-greedy dotall patterns.
**Action:** Replace `re.sub` for simple matched token/enclosure stripping with a fast linear scan using C-level `str.find()`. By matching `{` and `}` sequentially using `find()`, we can achieve a linear-time $O(N)$ parser that runs in milliseconds, is completely immune to catastrophic backtracking, and consumes far less memory.
