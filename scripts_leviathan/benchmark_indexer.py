import time
import os
from unittest.mock import MagicMock
import sys

# Simulation of the original truncation logic
def original_truncation(contenido):
    if len(contenido.split()) > 40000:
        contenido = " ".join(contenido.split()[:40000])
    return contenido

# Simulation of the proposed truncation logic
def optimized_truncation(contenido):
    words = contenido.split(None, 40001)
    if len(words) > 40000:
        contenido = " ".join(words[:40000])
    return contenido

def benchmark():
    print("--- Truncation Benchmark ---")
    # Generate a dummy document with 100,000 words
    dummy_doc = "word " * 100000

    start = time.time()
    for _ in range(10):
        original_truncation(dummy_doc)
    end = time.time()
    print(f"Original truncation (10x 100k words): {end - start:.4f}s")

    start = time.time()
    for _ in range(10):
        optimized_truncation(dummy_doc)
    end = time.time()
    print(f"Optimized truncation (10x 100k words): {end - start:.4f}s")

    print("\n--- Indexing Simulation (Batching) ---")
    # Simulate 200 documents
    num_docs = 200

    # Original: one by one
    start = time.time()
    mock_collection = MagicMock()
    for i in range(num_docs):
        mock_collection.add(
            documents=["content"],
            metadatas=[{"source": "doc"}],
            ids=[f"id_{i}"]
        )
    end = time.time()
    print(f"Original indexing (200 calls): {end - start:.4f}s (overhead simulation only)")

    # Optimized: batching (simulated)
    start = time.time()
    mock_collection = MagicMock()
    batch_size = 50
    for i in range(0, num_docs, batch_size):
        mock_collection.add(
            documents=["content"] * batch_size,
            metadatas=[{"source": "doc"}] * batch_size,
            ids=[f"id_{j}" for j in range(i, i + batch_size)]
        )
    end = time.time()
    print(f"Optimized indexing (4 calls): {end - start:.4f}s (overhead simulation only)")

if __name__ == "__main__":
    benchmark()
