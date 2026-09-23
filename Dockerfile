FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies including gnupg, curl, git, build-essential
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud CLI with de-armored GPG key
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && apt-get install -y --no-install-recommends \
    google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy files and install python dependencies
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "scripts_leviathan/12_auto_nexus_researcher.py"]
