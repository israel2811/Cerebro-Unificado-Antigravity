FROM python:3.11-slim-bookworm

# Prevent CI build hangs by setting non-interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for RAG and Google Cloud SDK
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK with GPG de-armoring fix
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && apt-get install -y google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# Install Python RAG dependencies
RUN pip install --no-cache-dir \
    chromadb \
    sentence-transformers \
    beautifulsoup4 \
    pydantic \
    aiofiles \
    networkx \
    matplotlib

# Set up workspace
WORKDIR /app
COPY . .

# Default command
CMD ["python3", "scripts_leviathan/04_chromadb_rag_indexer.py"]
