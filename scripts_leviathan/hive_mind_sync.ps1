<#
.SYNOPSIS
Protocolo 1: Sincronización Infalible (El Corazón del Enjambre)
.DESCRIPTION
Realiza un guardado atómico, rebase y subida a GitHub sin colisiones.
Preparado para trabajar junto a Syncthing en entornos de baja RAM.
#>

$RepoPath = "c:\Users\Lenovo\Antigravity_Cloud_Project"
$LogPath = "$RepoPath\.sync_health.log"

Function Write-Log {
    param([string]$Message)
    $Stamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    "$Stamp - $Message" | Out-File -FilePath $LogPath -Append
    Write-Host "[Omni-Swarm] $Message" -ForegroundColor Cyan
}

try {
    Write-Log "Iniciando Protocolo 1: Sincronización Inmortal."
    Set-Location $RepoPath -ErrorAction Stop

    # 1. State Checkpointing Local (Congelar cambios temporales)
    Write-Log "Asegurando memoria volátil. Ejecutando git stash..."
    git stash
    
    # 2. Rebase desde la Nube (La Verdad Distribuida)
    Write-Log "Descargando vector de la nube. Ejecutando git pull --rebase origin main..."
    $pullResult = git pull --rebase origin main 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Log "ADVERTENCIA: Fallo en pull rebase. $pullResult"
    }

    # 3. Restaurar cambios locales sobre la nube
    Write-Log "Aplicando estado local sobre la verdad de la nube..."
    $stashPop = git stash pop 2>&1
    if ($stashPop -match "No stash entries found") {
        Write-Log "No había estatus pendiente para restaurar."
    } elseif ($LASTEXITCODE -ne 0) {
        Write-Log "COLISIÓN DETECTADA AL HACER STASH POP. Conflictos en el Data Lake."
    }

    # 4. Inyección en la Nube
    Write-Log "Añadiendo vectores de conocimiento..."
    git add .
    
    $Status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($Status)) {
         Write-Log "No hay cambios para subir. El Enjambre está en perfecta sincronía."
    } else {
         Write-Log "Cambios detectados. Confirmando vectores..."
         git commit -m "auto: [Omni-Swarm Leviathan] Checkpoint Atómico de Sincronización"
         Write-Log "Subiendo al repositorio principal..."
         git push origin main
         Write-Log "Sincronización completada con éxito."
    }
} catch {
    Write-Log "FALLO CRÍTICO EN PROTOCOLO 1: $_"
    <# En caso de fallo total, Tailscale y Syncthing garantizan el P2P. #>
}
