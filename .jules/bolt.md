## 2026-06-14 - [Python String Truncation and ChromaDB Batching]
**Learning:** In Python, `len(s.split())` followed by `s.split()[:N]` scans the entire string twice and creates two large intermediate lists. Using `s.split(None, N+1)` scans only up to the Nth word, reducing execution time by ~140x for large documents. Additionally, batching ChromaDB `collection.add` calls significantly reduces transaction overhead.
**Action:** Always use `maxsplit` in `split()` for truncation and implement batching for vector database insertions.

## 2026-06-14 - [Docker Build and GitHub Actions Deprecation]
**Learning:** CI builds failed because the Dockerfile was located in `.devcontainer/Dockerfile` rather than the root, but the workflow didn't specify the `file` path. Also, Node.js 20 deprecation warnings require upgrading actions to latest semantic versions (e.g., v3, v4, v6).
**Action:** Always specify the `file` path in `docker/build-push-action` if the Dockerfile is not at the root. Use stable semantic tags for GitHub Actions to ensure forward compatibility with Node.js 24.

## 2026-06-14 - [GPG Key Handling in Docker (Debian Bookworm)]
**Learning:** When adding the Google Cloud SDK repo in a Debian Bookworm environment, the GPG key must be explicitly de-armored using `gpg --dearmor` if it's being used via the `signed-by` option in the sources list. Failing to do so causes `apt-get update` to fail with "public key is not available". Also, `gnupg` must be pre-installed.
**Action:** To successfully install the Google Cloud CLI in the project's Docker environment (Debian Bookworm), the GPG key must be explicitly de-armored: 'curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg' and 'gnupg' must be pre-installed via apt-get.
