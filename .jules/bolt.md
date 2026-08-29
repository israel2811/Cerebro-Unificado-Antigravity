
## 2026-07-12 - [Optimized ChromaDB Indexing]
**Learning:** Redundant `split()` calls on large strings are O(N) bottlenecks. Using `maxsplit` in `split(None, LIMIT)` avoids full-string processing when only a prefix is needed. Additionally, single-document vector insertions suffer from high API/process overhead.
**Action:** Always prefer batching for vector database insertions and use `maxsplit` for early-exit string processing in Python.

## 2026-07-12 - [CI Fix: Missing Dockerfile]
**Learning:** The CI workflow `docker-publish.yml` requires a root-level `Dockerfile`. If it's missing, the build will fail.
**Action:** Always ensure a production-ready `Dockerfile` and `requirements.txt` exist in the root if a Docker-based CI is active.
