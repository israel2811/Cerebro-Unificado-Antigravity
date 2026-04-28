## 2024-04-28 - Preventing Poisoned Batches in Data Pipelines
**Learning:** When implementing batch processing (e.g., in ChromaDB or Bulk API calls), failing to reset the batch state in a `finally` block after an error leads to "poisoned batches". Subsequent valid items are appended to a failing batch, causing cascading failures and data loss for the rest of the execution.
**Action:** Always wrap batch-add operations in a `try...except...finally` block. The `finally` block must clear the batch lists (`batch_docs`, etc.) to ensure the pipeline recovers and continues with fresh data.
