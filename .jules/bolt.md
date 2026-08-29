# ⚡ Bolt's Performance Journal

This journal tracks critical performance learnings, bottlenecks, and architectural patterns discovered in the Antigravity Unified Cloud Project.

## 2026-04-30 - Python String Split Performance
**Learning:** `str.split()` on large text buffers (e.g., 17MB corpus) is CPU-bound and significantly slower than `len(str)`. Benchmarking showed `len(s.split())` takes ~2.4s for 4M words, while `len(s)` is near-instant.
**Action:** Use character-length heuristics as a first-pass pre-filter before performing expensive `split()` or word-count operations on large documents.

## 2026-04-30 - ChromaDB Batching Efficiency
**Learning:** Individual `collection.add()` calls in ChromaDB incur significant per-call overhead. Batching multiple documents into a single call allows the underlying vector store to optimize I/O and vectorized embedding operations.
**Action:** Always implement batching (e.g., BATCH_SIZE=50) when indexing multiple documents into ChromaDB.
