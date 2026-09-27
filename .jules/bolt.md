# Bolt's Performance Journal

## 2026-03-31 - [Batching ChromaDB Document Inserts]
**Learning:** Inserting documents individually into ChromaDB in a loop incurs repeated model inference call setup, SQLite transaction locks, and disk write overhead. Batching document insertions into chunks of 20 speeds up processing up to 20x.
**Action:** Always batch document insertions when populating vector databases like ChromaDB.
