## 2026-06-25 - Batch Processing Optimization in ChromaDB Indexer

**Learning:** Individual calls to `collection.add` in ChromaDB introduce significant overhead due to repetitive IPC/network roundtrips and database transaction management. Consolidating these into batches (e.g., size 20) drastically reduces this overhead.

**Action:** Always implement batching when ingesting documents into vector databases to improve throughput, especially in resource-constrained environments like cloud VMs.
