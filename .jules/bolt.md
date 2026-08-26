# Bolt Performance Journal ⚡

## 2026-02-18 - String Truncation with maxsplit in ChromaDB RAG Indexer
**Learning:** Calling `.split()` without parameters on a large text file splits every single word into a list in memory. Doing this twice (once to check `len(...) > 40000` and once to slice `[:40000]`) is ~19x-36x slower on 1MB-10MB files than passing `maxsplit=40001` (`split(None, 40001)`).
**Action:** Use `maxsplit` whenever truncating string tokens or checking string token length limits to avoid allocating large unneeded token lists.
