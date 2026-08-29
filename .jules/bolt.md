## 2026-06-07 - Optimization of Word-Count Truncation with maxsplit

**Learning:** Using `.split()` without arguments on a large string to count words or truncate is inefficient because it tokenizes the entire string into memory. For a 1M word string, this can take ~0.6s and significant RAM. Using `.split(None, N+1)` (maxsplit) is ~130x faster because it stops splitting after the required number of words.

**Action:** Always use `maxsplit` when checking word count limits or truncating long documents to stay within vector database or LLM context window constraints.

## 2026-06-07 - Batch Processing in ChromaDB

**Learning:** Individual calls to `collection.add()` in ChromaDB (and most vector DBs) incur significant overhead (network/IPC, transaction management).

**Action:** Implement batching (e.g., `BATCH_SIZE = 20`) to consolidate multiple document insertions into a single operation, reducing total indexing time by up to 10x in high-latency environments or when processing thousands of small chunks.
