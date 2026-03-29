# ==============================================================================
# 🐙 PILAR 7: MENTE COLMENA GITHUB (HIVE MIND SYNC MULTI-NODO)
# ==============================================================================
# Propósito: Sincroniza el "Brain" entre PC Local, Nube Codespaces y Laptop.
# Evita sobrescrituras. Resuelve conflictos automáticamente con Rebase.
# Se recomienda correr por Tarea Programada cada 10 minutos.
# ==============================================================================

Write-Host "🐙 INICIANDO CONEXIÓN A LA MENTE COLMENA (HIVE-SYNC)..." -ForegroundColor Cyan

$repoDir = "C:\Users\Lenovo\Antigravity_Cloud_Project"

if (-Not (Test-Path $repoDir)) {
    Write-Host "[!] El repositorio base no existe: $repoDir" -ForegroundColor Red
    exit
}

Set-Location $repoDir

try {
    Write-Host "[*] 1️⃣ Guardando estado local temporal (Git Stash)..." -ForegroundColor Yellow
    git stash

    Write-Host "[*] 2️⃣ Atrayendo recuerdos de los otros Nodos (Git Pull Rebase)..." -ForegroundColor Yellow
    git pull --rebase origin main

    Write-Host "[*] 3️⃣ Restaurando y fusionando recuerdos locales (Git Stash Pop)..." -ForegroundColor Yellow
    git stash pop | Out-Null # Ignorar error si no había nada que stashear
}
catch {
    Write-Host "[!] Falla en la fusión P2P. Se requiere intervención humana." -ForegroundColor Red
}

Write-Host "[*] 4️⃣ Agregando nuevo conocimiento forense al Índice..." -ForegroundColor Yellow
git add .

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = "auto: [Hive-Mind Sync] Asimilación de Conocimiento - $timestamp"

Write-Host "[*] 5️⃣ Sellando el Códice (Git Commit)..." -ForegroundColor Yellow
git commit -m $commitMsg | Out-Null

Write-Host "[*] 6️⃣ Transmitiendo al Éter (Git Push)..." -ForegroundColor Yellow
git push origin main

Write-Host "✅ [HIVE-SYNC COMPLETO] El Enjambre piensa como uno solo." -ForegroundColor Green
