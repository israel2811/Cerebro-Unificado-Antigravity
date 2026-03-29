#!/bin/bash
# Antigravity Cloud Core - Startup Script
# Persists session state and auto-recovers work environment

# 1. Update and Install Dependencies
sudo apt-get update
sudo apt-get install -y git nodejs npm python3-pip

# 2. Clone/Pull Unified Repository
REPO_DIR="/home/antigravity/Cerebro-Unificado-Antigravity"
if [ ! -d "$REPO_DIR" ]; then
    git clone https://github.com/israel2811/Cerebro-Unificado-Antigravity.git "$REPO_DIR"
else
    cd "$REPO_DIR"
    git pull origin main
fi

# 3. Start N8N (Dockerless / Light Mode)
# Using npx to avoid heavy docker install if possible, or use standard install
# For now, placeholder for N8N start
# nohup npx n8n start --tunnel &

# 4. Notify Antigravity (Local)
# Curl to local machine if tunnel exists, or update a status file in repo
echo "Cloud Core Online: $(date)" > "$REPO_DIR/cloud_status.txt"
git -C "$REPO_DIR" add cloud_status.txt
git -C "$REPO_DIR" commit -m "Cloud VM Active"
git -C "$REPO_DIR" push origin main
