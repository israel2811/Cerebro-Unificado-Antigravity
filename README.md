# Antigravity Unified Cloud Setup

This repository contains the configuration for your Google Cloud Workstation and AI Agents.

## Setup Instructions

### PC 1 (This Machine)
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
2. Run `setup_cloud_migration.ps1` again.
3. Copy your project files into this folder.
4. Commit and push:
   ```powershell
   git add .
   git commit -m "Migration from PC 1"
   git push google main
   ```

### PC 2 (The Other Machine)
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
2. Clone this repository:
   ```powershell
   gcloud source repos clone antigravity-unified-cloud
   cd antigravity-unified-cloud
   ```
3. Create your branch:
   ```powershell
   git checkout -b pc2-legacy
   ```
4. Copy your PC 2 files into this folder.
5. Push:
   ```powershell
   git add .
   git commit -m "Migration from PC 2"
   git push origin pc2-legacy
   ```

## Configuration

- **.devcontainer**: Optimizes the environment for Google Cloud Workstations with Python, Node.js, and Google Cloud tools.
- **mcp_config.json**: Configures AI Agents (Jules, Anthropic, Gemini) and Google Drive access.
- **Port Forwarding**: Automatically forwards ports 3000 and 8080 to your local browser.

## Next Steps

Once both PC 1 and PC 2 have pushed their branches, go to Cloud Source Repositories and merge `pc2-legacy` into `main`. Then use the Cloud Workstation for development.
