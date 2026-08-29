# ⚡ Bolt's Performance Journal - Leviathan Project

## 2026-04-30 - ChromaDB Batch Indexing Bottleneck
**Learning:** Sequential calls to `collection.add()` for individual documents in `04_chromadb_rag_indexer.py` incur significant network/IPC overhead and miss out on vectorized embedding opportunities. In a constrained 2GB RAM environment, this inefficiency slows down the indexing of the 17MB corpus significantly.
**Action:** Always implement batch processing (e.g., BATCH_SIZE=50) for vector database insertions to optimize throughput. Use character-length heuristics as a pre-filter for expensive string operations like `.split()` to further reduce CPU load.

## 2026-04-30 - CI Build Failure: Missing Dockerfile
**Learning:** The GitHub Action workflow `.github/workflows/docker-publish.yml` defaults to looking for a `Dockerfile` in the repository root. This repository keeps its Dockerfile in `.devcontainer/Dockerfile`, causing CI build failures.
**Action:** When configuring Docker build actions in this repository, always explicitly set `file: .devcontainer/Dockerfile`. Avoid using specific commit SHAs for actions when stable versions (e.g., @v4) are available to simplify maintenance and resolve version resolution errors.

## 2026-04-30 - CI Build Failure: GPG Key De-armoring
**Learning:** Installing Google Cloud CLI via apt in a Dockerfile (Debian/Ubuntu) requires the GPG key to be de-armored if using the `signed-by` option in `sources.list`. Using a raw GPG key file results in `NO_PUBKEY` errors during `apt-get update`.
**Action:** Always use `curl ... | gpg --dearmor | tee /usr/share/keyrings/cloud.google.gpg` when adding the Google Cloud GPG key to ensure `apt` can correctly verify the repository signature.
