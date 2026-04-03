## 2025-05-15 - [ChromaDB Indexing Batching]
**Learning:** For vector database indexing (ChromaDB), using batching (e.g., BATCH_SIZE = 50) significantly optimizes network/IPC overhead and enables vectorized embedding operations. Given the 2GB RAM constraint, a 'flush' step after the main loop and using try-finally blocks are essential to ensure batch state is cleared and memory is managed efficiently.
**Action:** Always implement batch processing with a 'flush' and try-finally mechanism when performing bulk database operations to maximize performance within memory limits.

## 2025-05-15 - [CI Dockerfile Path]
**Learning:** The project's primary Dockerfile is located at `.devcontainer/Dockerfile`. CI/CD workflows using Docker must explicitly point to this file path as the default build context often expects it at the root.
**Action:** Ensure `docker-publish.yml` (or similar build scripts) uses the `file: .devcontainer/Dockerfile` argument when building the image.
