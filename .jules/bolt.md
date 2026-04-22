# Bolt's Performance Journal ⚡

This journal documents critical performance learnings and patterns discovered in the Antigravity Unified Cloud Setup.

## 2026-04-13 - Batching and Heuristic Filtering in ChromaDB
**Learning:** ChromaDB indexing was performed item-by-item, leading to high overhead. Additionally, expensive string splitting was performed on every file for word-count limiting.
**Action:** Implement batching (BATCH_SIZE=50) to optimize network/IPC overhead and use a character-length heuristic (150k chars) before splitting strings to reduce CPU usage.
