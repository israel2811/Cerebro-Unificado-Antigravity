#!/bin/bash
# ==============================================================================
# 🧠 NODO CEREBRO (GCP - e2-micro / 24/7 Zero Cost)
# ==============================================================================
# Instala Tailscale y configura los cronjobs del Omni-Swarm.
# ==============================================================================

echo "🚀 Iniciando Forja del Nodo Cerebro en GCP..."

# 1. Actualizar repositorios e instalar dependencias básicas
sudo apt update && sudo apt install -y curl tmux git python3-pip cron

# 2. Descargar e instalar Tailscale (Malla Zero-Trust)
echo "🌐 Instalando Tailscale (Malla P2P)..."
curl -fsSL https://tailscale.com/install.sh | sh

# 3. Levantar Tailscale
echo "🔑 Por favor, autentica Tailscale:"
sudo tailscale up

# 4. Configuración del Insomnia Hack (Ping a Hugging Face)
echo "⏰ Configurando Crontab para Insomnia Hack..."

cat << 'EOF' > ~/insomnia_hack.sh
#!/bin/bash
TARGET_URL="https://israelrealivazquez2811-nexus-sentinel.hf.space"
HTTP_RESPONSE=$(curl --write-out "%{http_code}" --silent --output /dev/null "$TARGET_URL")
if [ "$HTTP_RESPONSE" -eq 200 ]; then echo "OK"; fi
EOF

chmod +x ~/insomnia_hack.sh

# Agregar al crontab si no existe
(crontab -l 2>/dev/null | grep -v "insomnia_hack.sh" ; echo "*/15 * * * * ~/insomnia_hack.sh") | crontab -

echo "✅ Nodo Cerebro de GCP Configurado y Vivo."
echo "▶️ Para ver la IP interna de la malla: tailscale ip -4"
