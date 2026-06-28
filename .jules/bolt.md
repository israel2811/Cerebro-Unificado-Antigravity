
## 2026-06-21 - [ChromaDB Indexer Optimization]
**Learning:** Batching `collection.add` calls significantly reduces the overhead of vector database ingestion. Additionally, using `split(None, N+1)` is much more efficient than multiple full-string `split()` calls for large text files.
**Action:** Always implement batching for vector ingestion and use `maxsplit` in string operations when dealing with large corpora to avoid memory spikes and redundant processing.

## 2026-06-21 - [CI Build Failure: Missing Dockerfile]
**Learning:** The GitHub Actions workflow `docker-publish.yml` expects a `Dockerfile` in the root directory to build the production image. Relying only on `.devcontainer/Dockerfile` is insufficient for CI pipelines that target production artifacts.
**Action:** Always ensure a root-level `Dockerfile` exists if a CI/CD pipeline is configured to build and push images. Added a minimal production Dockerfile to resolve the "no such file or directory" error in buildx.
