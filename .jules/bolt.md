# Bolt's Performance Journal

## 2026-06-15 - Optimizing String Truncation in Python
**Learning:** Using `string.split()` without arguments on a large string to count words and then slicing the resulting list is extremely inefficient because it creates a full list of all words in memory. Using `string.split(None, maxsplit=N)` is significantly faster as it stops splitting after N words.
**Action:** Always use `maxsplit` when only a prefix of words is needed for truncation or validation.

## 2026-06-15 - Batching ChromaDB Additions
**Learning:** Individual calls to `collection.add` in ChromaDB incur significant overhead per document (serialization, IPC/network, disk I/O).
**Action:** Implement batching for `collection.add` to improve ingestion throughput.

## 2026-06-15 - State Management in Batching Functions
**Learning:** When using nested helper functions to flush batches, using `.clear()` on shared lists can cause issues with unit tests if mocks capture the list by reference.
**Action:** Reassign batch lists (e.g., `batch_docs = []`) using `nonlocal` to ensure mocks capture the state of the list at the time of the call and to properly reset the state.
