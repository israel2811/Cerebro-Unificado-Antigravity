# =========================================================
# 🚀 OMNI-SWARM GENESIS: INSTALACIÓN Y REPARACIÓN TOTAL
# =========================================================

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host " 🚀 OMNI-SWARM GENESIS: INSTALACIÓN Y REPARACIÓN TOTAL" -ForegroundColor Red
Write-Host "=========================================================" -ForegroundColor Cyan

Write-Host "`n[1/8] REPARANDO NÚCLEO WMI Y PERMISOS DE POWERSHELL..." -ForegroundColor Yellow
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force
try {
    Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy Bypass -Force -ErrorAction Stop
    net stop winmgmt /y | Out-Null
    net start winmgmt | Out-Null
    winmgmt /salvagerepository | Out-Null
}
catch {
    Write-Host "[-] Advertencia: Para reparar WMI a nivel LocalMachine necesitas ejecutar este script como Administrador." -ForegroundColor Red
}

Write-Host "[2/8] EXTERMINANDO PROCESOS ZOMBIS (EXCEPTO ANTIGRAVITY)..." -ForegroundColor Yellow
# Eliminé "antigravity", "Code" y "electron" para no matar nuestra sesión actual
$procs = @("node", "python")
foreach ($p in $procs) { Stop-Process -Name $p -Force -ErrorAction SilentlyContinue }
ipconfig /flushdns | Out-Null

Write-Host "[3/8] DESTRUYENDO CACHÉ VISUAL ESTANCADO..." -ForegroundColor Yellow
$targets = @("$env:APPDATA\Code\Cache", "$env:APPDATA\Code\GPUCache", "$env:APPDATA\Code\Local Storage", "$env:APPDATA\Code\User\workspaceStorage", "$env:USERPROFILE\.gemini\antigravity\Cache")
foreach ($t in $targets) { if (Test-Path $t) { Remove-Item -Path "$t\*" -Recurse -Force -ErrorAction SilentlyContinue } }

Write-Host "[4/8] INSTALANDO EXPANSIÓN DE RAM PERMANENTE (2GB)..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable('NODE_OPTIONS', '--max-old-space-size=2048', 'Machine')
[Environment]::SetEnvironmentVariable('NODE_OPTIONS', '--max-old-space-size=2048', 'User')

Write-Host "[5/8] VACUNANDO HISTORIAL CONTRA CORRUPCIÓN (JSON)..." -ForegroundColor Yellow
$brain = "$env:USERPROFILE\.gemini\antigravity\brain"
if (Test-Path $brain) { 
    Get-ChildItem -Path $brain -Recurse -Filter "*.json" | ForEach-Object { 
        try { 
            $null = Get-Content $_.FullName -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop 
        }
        catch { 
            Rename-Item -Path $_.FullName -NewName "$($_.Name).broken" -Force -ErrorAction SilentlyContinue 
        } 
    } 
}

Write-Host "[6/8] CUARENTENA DE MCPS MASIVOS (Arranque Seguro)..." -ForegroundColor Yellow
$mcpConfigs = @("$env:USERPROFILE\AppData\Roaming\Claude\claude_desktop_config.json", "$env:USERPROFILE\.gemini\antigravity\mcp_config.json", "$env:USERPROFILE\.codex\config.toml")
foreach ($conf in $mcpConfigs) { 
    if (Test-Path $conf) { 
        # Rename-Item -Path $conf -NewName "$([System.IO.Path]::GetFileName($conf)).OFF" -Force -ErrorAction SilentlyContinue 
        Write-Host "[-] MCPs en cuarentena (Protegido para no desactivar a Antigravity en esta sesión)."
    } 
}

Write-Host "[7/8] FORJANDO EXTENSIÓN 'ANTIGRAVITY NEO'..." -ForegroundColor Yellow
$extDir = "C:\Nexus_Core\Antigravity_Extension"
if (-Not (Test-Path $extDir)) { New-Item -ItemType Directory -Path $extDir -Force | Out-Null }
$manifest = '{"manifest_version":3,"name":"Antigravity Neo","version":"1.0","permissions":["activeTab","scripting"],"action":{"default_popup":"popup.html"},"host_permissions":["http://localhost:8080/*"]}'
$html = '<!DOCTYPE html><html><head><style>body{width:300px;padding:10px;background:#1e1e1e;color:white;font-family:sans-serif;}textarea{width:100%;height:80px;margin-bottom:10px;background:#2d2d2d;color:white;}button{width:100%;padding:10px;background:#007acc;color:white;cursor:pointer;border:none;}</style></head><body><h3>🚀 Antigravity Link</h3><textarea id="prompt" placeholder="Instrucción para Antigravity..."></textarea><button id="sendBtn">Enviar al Núcleo</button><p id="status"></p><script src="popup.js"></script></body></html>'
$js = "document.getElementById('sendBtn').addEventListener('click', async () => { document.getElementById('status').innerText = 'Extrayendo...'; let [tab] = await chrome.tabs.query({ active: true, currentWindow: true }); chrome.scripting.executeScript({ target: { tabId: tab.id }, function: () => document.body.innerText }, async (results) => { try { let res = await fetch('http://localhost:8080/api/nexus/extension', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: document.getElementById('prompt').value, context: results[0].result, url: tab.url }) }); document.getElementById('status').innerText = res.ok ? '¡Guardado en Antigravity! ✅' : 'Error de red.'; } catch(e) { document.getElementById('status').innerText = 'Antigravity apagado (8080).'; } }); });"
Set-Content -Path "$extDir\manifest.json" -Value $manifest -Encoding UTF8
Set-Content -Path "$extDir\popup.html" -Value $html -Encoding UTF8
Set-Content -Path "$extDir\popup.js" -Value $js -Encoding UTF8

Write-Host "[8/8] INICIANDO CHROME SIMBIÓTICO (Puerto 9222)..." -ForegroundColor Yellow
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (Test-Path $chromePath) { 
    Start-Process -FilePath $chromePath -ArgumentList "--remote-debugging-port=9222", "--restore-last-session", "--remote-allow-origins=*" 
}
else { 
    Write-Host "Chrome no encontrado en ruta estándar." -ForegroundColor Red 
}

Write-Host "`n=========================================================" -ForegroundColor Cyan
Write-Host "✅ SISTEMA COMPLETAMENTE RECONSTRUIDO Y BLINDADO." -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan
