## 2026-07-16 - Efficient String Truncation in Python
**Learning:** Using `.split()` without arguments on a large string to check word count followed by another `.split()[:N]` is O(N) but with a large constant factor because it allocates a full list of all words twice. Using `.split(None, N+1)` (maxsplit) avoids splitting the entire string if only the first N words are needed.
**Action:** Always use `maxsplit` when truncating strings by word count to save memory and CPU.

## 2026-07-16 - ChromaDB Batching
**Learning:** Individual `collection.add()` calls in ChromaDB (and most vector DBs) have significant overhead. Batching documents (e.g., size 20-100) significantly improves throughput.
**Action:** Implement batching for all vector database ingestion tasks.

## 2026-07-16 - Missing Dockerfile in CI
**Learning:** GitHub Actions workflows (like docker-publish.yml) that rely on building a Docker image will fail if the `Dockerfile` is missing from the root or context directory specified.
**Action:** Always ensure a valid `Dockerfile` is present when configuring Docker-based CI/CD.
