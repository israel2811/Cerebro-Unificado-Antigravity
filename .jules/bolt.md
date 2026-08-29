## 2025-04-17 - ChromaDB Batching and String Heuristics
**Learning:** For vector database indexing (ChromaDB), switching from individual `collection.add()` calls to batched calls (BATCH_SIZE=50) significantly reduces IPC/network overhead. Additionally, using a character-length heuristic (e.g., `len(text) < 150000`) before performing expensive `.split()` operations for word-count limits provides a measurable speedup for smaller chunks while remaining safe for large ones.
**Action:** Always implement batching for vector DB ingestion and use fast pre-filters (like string length) before CPU-intensive text processing.

## 2025-04-17 - Docker CI and GPG Key Fixes
**Learning:** The project's GitHub Actions workflow (`docker-publish.yml`) expects a root-level `Dockerfile`. Additionally, installing the Google Cloud CLI via APT requires dearmoring the GPG key with `gpg --dearmor` to avoid signature verification failures (NO_PUBKEY) in newer Ubuntu environments.
**Action:** Always maintain a root-level `Dockerfile` for CI and use proper GPG key handling in Dockerfiles.
