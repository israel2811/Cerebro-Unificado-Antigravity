FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js and system build tools
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && apt-get install -y nodejs build-essential git gnupg curl

# Install Google Cloud SDK with gpg --dearmor
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && apt-get install -y google-cloud-cli

WORKDIR /workspace

# Copy requirements and install dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /workspace/
