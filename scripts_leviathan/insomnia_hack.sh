#!/bin/bash
# ==============================================================================
# INSOMNIA HACK - HUGGING FACE SENTINEL (Pilar 3)
# ==============================================================================
# Propósito: Mantiene el Space de Hugging Face (16GB RAM) despierto 24/7.
# Ejecución: Debe cargarse en el crontab de Google Cloud Shell (ej. e2-micro).
# Frecuencia: Cada 15 minutos exactos (* /15 * * * *).
# ==============================================================================

TARGET_URL="https://israelrealivazquez2811-nexus-sentinel.hf.space"
LOG_FILE="$HOME/insomnia_hack.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Enviando Pulso de Vida (Ping) a Hugging Face Sentinel..." >> "$LOG_FILE"

# Llamada HTTP silenciosa pero con output de código de estado
HTTP_RESPONSE=$(curl --write-out "%{http_code}" --silent --output /dev/null "$TARGET_URL")

if [ "$HTTP_RESPONSE" -eq 200 ]; then
    echo "[$TIMESTAMP] EXITO. Contenedor HF de 16GB RAM Activo." >> "$LOG_FILE"
elif [ "$HTTP_RESPONSE" -eq 503 ]; then
    echo "[$TIMESTAMP] ADVERTENCIA. El contenedor está despertando de hibernación lenta (Cold Start)." >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ERROR CRITICO. Código de respuesta: $HTTP_RESPONSE. Revisar Hugging Face." >> "$LOG_FILE"
fi

# Instrucciones para el usuario:
# 1. Abre Google Cloud Shell
# 2. Sube este script y dale permisos: chmod +x insomnia_hack.sh
# 3. Abre crontab: crontab -e
# 4. Agrega la línea: */15 * * * * /home/tu_usuario/insomnia_hack.sh
