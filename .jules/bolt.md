
## 2026-05-07 - Streaming and Batching Optimization
**Learning:** Monolithic processing of large corpus files (17MB+) is a major memory bottleneck. Implementing a streaming generator for document extraction and batching for ChromaDB indexing (BATCH_SIZE=50) significantly improves stability and throughput.
**Action:** Always prefer streaming generators for large file I/O and batching for database operations. Use character-length heuristics as pre-filters for expensive string operations.
