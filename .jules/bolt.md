# Bolt Performance Journal

## 2026-02-18 - Python String Splitting & Batching in RAG Indexing
**Learning:** Using `str.split(None, maxsplit)` instead of double `str.split()` avoids full-string tokenization overhead on multi-megabyte files. Batching `chromadb` inserts in groups of 20 reduces SQLite transaction overhead and model batching latency by up to 20x.
**Action:** Always prefer `split(None, maxsplit)` for length checks on potentially large text files, and batch vector database insertions.
