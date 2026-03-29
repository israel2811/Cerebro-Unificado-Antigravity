# ==============================================================================
# 🌉 PILAR 4: TÚNEL ZERO-TRUST (CLOUDFLARE) PARA CHATGPT CUSTOM GPT
# ==============================================================================
# Propósito: Expone el Servidor MCP Local o el API Neo a ChatGPT de forma encriptada.
# Uso: Ejecutar localmente. La URL arrojada se ingresa en el config de OpenAI ChatGPT.
# ==============================================================================

Write-Host "🚀 INICIANDO EXCAVACIÓN DE TÚNEL ZERO-TRUST (CLOUDFLARE)..." -ForegroundColor Cyan

# 1. Instalar cloudflared si no está presente
$cloudflaredPath = "$env:USERPROFILE\.cloudflared\cloudflared.exe"
if (-Not (Test-Path $cloudflaredPath)) {
    Write-Host "[*] Descargando binario de Cloudflared (Túnel Inverso)..." -ForegroundColor Yellow
    $url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cloudflared" | Out-Null
    Invoke-WebRequest -Uri $url -OutFile $cloudflaredPath
}

# 2. Configurar el OpenAPI (Swagger) de Antigravity Neo
$openapiPath = "C:\Nexus_Core\openapi_chatgpt_config.json"
$openapiTemplate = @"
{
  "openapi": "3.1.0",
  "info": {
    "title": "Antigravity Neo MCP",
    "description": "Puente local entre ChatGPT y computadora del usuario. Permite inyectar contexto y leer el brain/ dir.",
    "version": "v1.0.0"
  },
  "servers": [
    {
      "url": "https://TU_URL_DE_CLOUDFLARE.trycloudflare.com",
      "description": "Túnel Dinámico Cloudflare"
    }
  ],
  "paths": {
    "/api/nexus/extension": {
      "post": {
        "operationId": "injectContext",
        "summary": "Inyectar data a Antigravity Local",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "prompt": { "type": "string" },
                  "context": { "type": "string" },
                  "url": { "type": "string" }
                }
              }
            }
          }
        },
        "responses": {
          "200": { "description": "Éxito" }
        }
      }
    }
  }
}
"@
Set-Content -Path $openapiPath -Value $openapiTemplate -Encoding UTF8
Write-Host "[+] Archivo Swagger (OpenAPI) para ChatGPT generado en: $openapiPath" -ForegroundColor Green

# 3. Levantar túnel apuntando al puerto 8080 (donde escucha nexus_ext_api.py)
Write-Host "[+] Abriendo túnel seguro hacia localhost:8080..." -ForegroundColor Yellow
Write-Host "⚠️ COPIA LA URL (.trycloudflare.com) QUE APARECERÁ ABAJO Y PÉGALA EN CHATGPT:" -ForegroundColor Red
Write-Host "   (Reemplaza 'TU_URL_DE_CLOUDFLARE' en el archivo openapi_chatgpt_config.json con ella)" -ForegroundColor Cyan
& $cloudflaredPath tunnel --url http://localhost:8080
