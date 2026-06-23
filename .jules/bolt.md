## 2026-06-23 - Optimized Vector Indexing & String Truncation
**Learning:** Individual `collection.add` calls in ChromaDB create significant network/IPC overhead. In contrast, batch processing reduces the number of roundtrips. Additionally, word-count truncation using `len(text.split())` followed by `" ".join(text.split()[:N])` performs two full passes over the string, which is highly inefficient for large documents.

**Action:** Implement batching (e.g., `BATCH_SIZE = 20`) for vector database injections and use `split(None, N+1)` with `maxsplit` to truncate strings in a single pass. Always remove `__pycache__` before PR submission to avoid committing binary artifacts.
