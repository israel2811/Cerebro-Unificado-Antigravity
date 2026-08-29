# Bolt's Performance Journal

This journal tracks critical performance learnings, bottlenecks, and optimizations discovered within the Antigravity Unified Cloud Setup.

## 2025-04-24 - Initial Discovery: ChromaDB Indexing Bottlenecks
**Learning:** The current indexing script `04_chromadb_rag_indexer.py` performs individual `collection.add()` calls for each document, which is inefficient due to IPC/network overhead. Additionally, it performs redundant `.split()` operations on every document to check for word limits, even for small files.
**Action:** Implement batch processing (BATCH_SIZE=50) and a character-length heuristic to avoid unnecessary string splitting.
