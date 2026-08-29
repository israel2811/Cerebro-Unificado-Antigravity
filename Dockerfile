FROM python:3.11-slim-bookworm

# Evitar prompts de apt
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema y herramientas necesarias
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Fix GPG de Google Cloud SDK (De-armored para evitar errores en CI)
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && apt-get install -y google-cloud-cli && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias de RAG
RUN pip install --no-cache-dir \
    chromadb \
    sentence-transformers \
    beautifulsoup4 \
    networkx \
    matplotlib

# Configurar el espacio de trabajo
WORKDIR /app

# Copiar el código del proyecto
COPY . .

# Comando por defecto
CMD ["python3", "scripts_leviathan/12_auto_nexus_researcher_v3.py"]
