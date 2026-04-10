# Bolt's Performance Journal

## 2026-04-10 - Optimized Vector Ingestion via Batching and Pre-filtering
**Learning:** ChromaDB indexing was bottlenecked by individual 'collection.add()' calls. Implementing batching (BATCH_SIZE=50) significantly reduces IPC overhead and enables vectorized embedding operations. Additionally, using character length as a pre-filter before 'split()' operations avoids O(N) memory allocation for small chunks.
**Action:** Always prefer batched insertions for vector databases and use cheap length checks before expensive string/list operations in text processing pipelines.
