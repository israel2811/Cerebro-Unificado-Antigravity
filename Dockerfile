# Build stage for RAG dependencies
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies for ChromaDB and Google Cloud SDK
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install RAG dependencies
RUN pip install --no-cache-dir chromadb sentence-transformers

# Copy only the necessary scripts
COPY scripts_leviathan/ /app/scripts_leviathan/

# Default command
CMD ["python3", "scripts_leviathan/04_chromadb_rag_indexer.py"]
