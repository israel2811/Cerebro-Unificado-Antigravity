FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs build-essential git

# Install Google Cloud SDK with robust GPG key handling
# Note: Google's apt repo uses multiple keys. Using apt-key add for broader compatibility in this environment.
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl && \
    echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-cli

# Set up workspace
WORKDIR /workspace
