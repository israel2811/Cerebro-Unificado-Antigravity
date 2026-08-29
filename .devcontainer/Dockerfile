FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Install Node.js and dependencies
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs build-essential git gnupg

# Install Google Cloud SDK
# Bolt Optimization: Properly de-armor GPG key to avoid NO_PUBKEY errors in CI
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor | tee /usr/share/keyrings/cloud.google.gpg > /dev/null && \
    apt-get update && apt-get install -y google-cloud-cli

# Set up workspace
WORKDIR /workspace
