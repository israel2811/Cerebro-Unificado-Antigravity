FROM python:3.11-slim-bookworm

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system essentials
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    git \
    build-essential \
    ca-certificates \
    apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK with correct GPG key handling (avoiding NO_PUBKEY errors)
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-cloud-cli && \
    rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all repository files
COPY . .

# Default entry point command
CMD ["python3", "scripts_leviathan/12_auto_nexus_researcher.py"]
