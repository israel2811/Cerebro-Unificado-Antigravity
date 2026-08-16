FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies required by Google Cloud SDK and build processes
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Fix GPG de-armoring for google-cloud-cli
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies list first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default entry point
CMD ["python", "scripts_leviathan/12_auto_nexus_researcher.py"]
