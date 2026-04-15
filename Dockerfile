FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js 20 and essentials
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs build-essential git gnupg curl && \
    rm -rf /var/lib/apt-get/lists/*

# Install Google Cloud SDK with correct GPG key handling (avoiding NO_PUBKEY errors)
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && \
    apt-get install -y google-cloud-cli && \
    rm -rf /var/lib/apt-get/lists/*

# Set up workspace
WORKDIR /workspace

# Copy files
COPY . .

# Default command
CMD ["bash"]
