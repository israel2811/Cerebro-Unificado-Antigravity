FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs build-essential git

# Install Google Cloud SDK with robust GPG key handling
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && apt-get install -y google-cloud-cli

# Set up workspace
WORKDIR /workspace
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir chromadb sentence-transformers beautifulsoup4 networkx matplotlib

CMD ["bash"]
