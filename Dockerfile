FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs build-essential git

# Install Google Cloud SDK
# BOLT OPTIMIZATION: Use gpg --dearmor for the GPG key to prevent NO_PUBKEY errors in APT
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && apt-get install -y google-cloud-cli

# Set up workspace
WORKDIR /workspace
