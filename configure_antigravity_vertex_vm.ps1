param(
    [string]$VertexApiKey = "",
    [string]$ProjectId = "",
    [string]$Region = "us-central1",
    [string]$Zone = "us-central1-a",
    [string]$InstanceName = "antigravity-hyper",
    [int]$BootDiskGb = 200,
    [string]$BootDiskType = "pd-ssd",
    [int]$DataDiskGb = 2048,
    [string]$DataDiskType = "pd-standard",
    [string]$DataDiskName = "",
    [string]$WorkspacePath = "C:\Users\Lenovo\Antigravity_Cloud_Project",
    [string]$MachineType = "",
    [switch]$SkipVm
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[step] $Message" -ForegroundColor Cyan
}

function Add-UserPath {
    param([string]$PathToAdd)
    if (-not $PathToAdd -or -not (Test-Path $PathToAdd)) {
        return
    }

    $currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if (-not $currentUserPath) {
        $currentUserPath = ""
    }

    $segments = $currentUserPath.Split(";", [System.StringSplitOptions]::RemoveEmptyEntries)
    if ($segments -contains $PathToAdd) {
        return
    }

    $newPath = if ([string]::IsNullOrWhiteSpace($currentUserPath)) {
        $PathToAdd
    } else {
        "$currentUserPath;$PathToAdd"
    }

    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    $env:Path = "$env:Path;$PathToAdd"
}

function Get-GcloudPath {
    $candidates = @(
        "C:\Users\$env:USERNAME\GoogleCloudSDK\google-cloud-sdk\bin\gcloud.cmd",
        "$env:ProgramFiles\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
        "${env:ProgramFiles(x86)}\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    )

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path $candidate)) {
            return $candidate
        }
    }

    $existing = Get-Command gcloud -ErrorAction SilentlyContinue
    if ($existing) {
        return $existing.Source
    }

    throw "No se encontro gcloud. Instala Google Cloud SDK antes de continuar."
}

function Invoke-Gcloud {
    param(
        [string[]]$CommandArgs,
        [switch]$IgnoreExitCode
    )
    & $script:GcloudPath @CommandArgs
    $code = $LASTEXITCODE
    if (-not $IgnoreExitCode -and $code -ne 0) {
        throw "gcloud fallo ($code): gcloud $($CommandArgs -join ' ')"
    }
    return $code
}

function Invoke-GcloudCapture {
    param([string[]]$CommandArgs)

    $nativeBehaviorExists = $null -ne (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue)
    if ($nativeBehaviorExists) {
        $previousNativeBehavior = $PSNativeCommandUseErrorActionPreference
        $global:PSNativeCommandUseErrorActionPreference = $false
    }

    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"

    try {
        $output = @()
        $exitCode = 0
        try {
            $output = & $script:GcloudPath @CommandArgs 2>&1
            $exitCode = $LASTEXITCODE
        } catch {
            $exitCode = if ($LASTEXITCODE -ne 0) { $LASTEXITCODE } else { 1 }
            $output = @()
        }

        return [pscustomobject]@{
            ExitCode = $exitCode
            Output   = (($output | ForEach-Object { "$_" }) -join "`n")
        }
    } finally {
        $ErrorActionPreference = $previousErrorAction
        if ($nativeBehaviorExists) {
            $global:PSNativeCommandUseErrorActionPreference = $previousNativeBehavior
        }
    }
}

function Ensure-FirewallRule {
    param(
        [string]$RuleName,
        [string[]]$RuleArgs
    )

    $describeResult = Invoke-GcloudCapture -CommandArgs @("compute", "firewall-rules", "describe", $RuleName, "--quiet")
    if ($describeResult.ExitCode -eq 0) {
        return
    }

    $createArgs = @("compute", "firewall-rules", "create", $RuleName) + $RuleArgs + @("--quiet")
    Invoke-Gcloud -CommandArgs $createArgs
}

function Ensure-VertexEnv {
    param(
        [string]$ApiKey,
        [string]$Project,
        [string]$RegionName
    )

    if ([string]::IsNullOrWhiteSpace($ApiKey)) {
        $ApiKey = [Environment]::GetEnvironmentVariable("VERTEX_API_KEY", "User")
    }

    if ([string]::IsNullOrWhiteSpace($ApiKey)) {
        Write-Host "[warn] No se recibio API key para Vertex. Configura VERTEX_API_KEY luego." -ForegroundColor Yellow
        return
    }

    [Environment]::SetEnvironmentVariable("VERTEX_API_KEY", $ApiKey, "User")
    [Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", $ApiKey, "User")
    [Environment]::SetEnvironmentVariable("ANTIGRAVITY_VERTEX_API_KEY", $ApiKey, "User")
    [Environment]::SetEnvironmentVariable("GOOGLE_CLOUD_PROJECT", $Project, "User")
    [Environment]::SetEnvironmentVariable("GOOGLE_CLOUD_REGION", $RegionName, "User")

    $env:VERTEX_API_KEY = $ApiKey
    $env:GOOGLE_API_KEY = $ApiKey
    $env:ANTIGRAVITY_VERTEX_API_KEY = $ApiKey
    $env:GOOGLE_CLOUD_PROJECT = $Project
    $env:GOOGLE_CLOUD_REGION = $RegionName
}

function Update-McpConfigFile {
    param(
        [string]$ConfigPath,
        [string]$FilesystemRoot
    )

    $configDir = Split-Path $ConfigPath -Parent
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }

    if (Test-Path $ConfigPath) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        Copy-Item $ConfigPath "$ConfigPath.bak.$stamp" -Force
    }

    $config = $null
    if (Test-Path $ConfigPath) {
        try {
            $content = Get-Content $ConfigPath -Raw
            $config = $content | ConvertFrom-Json
        } catch {
            Write-Host "[warn] No se pudo parsear $ConfigPath, se recreara." -ForegroundColor Yellow
        }
    }

    if (-not $config) {
        $config = [pscustomobject]@{
            mcpServers = [pscustomobject]@{}
        }
    }

    if (-not $config.mcpServers) {
        $config | Add-Member -NotePropertyName mcpServers -NotePropertyValue ([pscustomobject]@{}) -Force
    }

    $config.mcpServers.filesystem = [pscustomobject]@{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-filesystem", $FilesystemRoot)
    }

    if (-not $config.mcpServers.'google-drive') {
        $config.mcpServers | Add-Member -NotePropertyName "google-drive" -NotePropertyValue (
            [pscustomobject]@{
                command = "npx"
                args = @("-y", "@modelcontextprotocol/server-google-drive")
                env = [pscustomobject]@{
                    GOOGLE_DRIVE_FOLDER_ID = "REPLACE_WITH_FOLDER_ID"
                }
            }
        ) -Force
    }

    if (-not $config.mcpServers.memory) {
        $config.mcpServers | Add-Member -NotePropertyName "memory" -NotePropertyValue (
            [pscustomobject]@{
                command = "npx"
                args = @("-y", "@modelcontextprotocol/server-memory")
            }
        ) -Force
    }

    if (-not $config.mcpServers.everything) {
        $config.mcpServers | Add-Member -NotePropertyName "everything" -NotePropertyValue (
            [pscustomobject]@{
                command = "npx"
                args = @("-y", "@modelcontextprotocol/server-everything")
            }
        ) -Force
    }

    $json = $config | ConvertTo-Json -Depth 25
    $json | Set-Content -Path $ConfigPath -Encoding UTF8
}

function Get-CandidateMachineTypes {
    param(
        [string]$ZoneName,
        [string]$PreferredMachineType
    )

    if (-not [string]::IsNullOrWhiteSpace($PreferredMachineType)) {
        return @($PreferredMachineType)
    }

    $raw = & $script:GcloudPath compute machine-types list --zones=$ZoneName --format=json
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo listar machine types en la zona $ZoneName."
    }

    $types = $raw | ConvertFrom-Json
    $filtered = $types | Where-Object { -not $_.isSharedCpu }

    $quotaRaw = & $script:GcloudPath compute project-info describe --format=json
    $quotaInfo = $quotaRaw | ConvertFrom-Json
    $cpuQuota = $quotaInfo.quotas | Where-Object { $_.metric -eq "CPUS_ALL_REGIONS" } | Select-Object -First 1
    if ($cpuQuota) {
        $availableCpus = [math]::Floor([double]$cpuQuota.limit - [double]$cpuQuota.usage)
        if ($availableCpus -gt 0) {
            $filtered = $filtered | Where-Object { [int]$_.guestCpus -le $availableCpus }
        }
    }
    $sorted = $filtered | Sort-Object @{Expression = "memoryMb"; Descending = $true}, @{Expression = "guestCpus"; Descending = $true}
    $topNames = $sorted | Select-Object -ExpandProperty name -First 40

    $preferred = @(
        "m3-ultramem-32",
        "n2d-standard-224",
        "n2-highmem-32",
        "n2-highmem-128",
        "n2-highmem-16",
        "n2-standard-32",
        "n2-standard-16",
        "c4-highcpu-32",
        "c4-highcpu-16",
        "c4-highcpu-48",
        "n2-standard-128",
        "n2-standard-64",
        "e2-standard-32",
        "e2-standard-16"
    )

    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($name in $preferred) {
        if ($topNames -contains $name) {
            $candidates.Add($name)
        }
    }
    foreach ($name in $topNames) {
        if (-not $candidates.Contains($name)) {
            $candidates.Add($name)
        }
        if ($candidates.Count -ge 12) {
            break
        }
    }
    return $candidates.ToArray()
}

Write-Step "Resolviendo gcloud"
$script:GcloudPath = Get-GcloudPath
$sdkBin = Split-Path $script:GcloudPath -Parent
$sdkRoot = Split-Path $sdkBin -Parent
$bundledPython = Join-Path $sdkRoot "platform\bundledpython\python.exe"

if (Test-Path $bundledPython) {
    $env:CLOUDSDK_PYTHON = $bundledPython
    Add-UserPath -PathToAdd (Split-Path $bundledPython -Parent)
}

$env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"
Add-UserPath -PathToAdd $sdkBin

Write-Step "Validando gcloud"
Invoke-Gcloud -CommandArgs @("--quiet", "version")

if ([string]::IsNullOrWhiteSpace($ProjectId)) {
    $ProjectId = (& $script:GcloudPath config get-value project 2>$null).Trim()
}
if ([string]::IsNullOrWhiteSpace($ProjectId) -or $ProjectId -eq "(unset)") {
    throw "No hay project activo en gcloud. Pasa -ProjectId o ejecuta gcloud config set project <ID>."
}

Write-Step "Configurando proyecto y region/zone"
Invoke-Gcloud -CommandArgs @("config", "set", "project", $ProjectId, "--quiet")
Invoke-Gcloud -CommandArgs @("config", "set", "compute/region", $Region, "--quiet")
Invoke-Gcloud -CommandArgs @("config", "set", "compute/zone", $Zone, "--quiet")

Write-Step "Habilitando APIs base"
Invoke-Gcloud -CommandArgs @(
    "services", "enable",
    "compute.googleapis.com",
    "aiplatform.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "--project", $ProjectId,
    "--quiet"
)

Write-Step "Guardando variables de Vertex/Google para Antigravity"
Ensure-VertexEnv -ApiKey $VertexApiKey -Project $ProjectId -RegionName $Region

if (-not (Test-Path $WorkspacePath)) {
    New-Item -ItemType Directory -Path $WorkspacePath -Force | Out-Null
}
$workspaceData = Join-Path $WorkspacePath "data"
if (-not (Test-Path $workspaceData)) {
    New-Item -ItemType Directory -Path $workspaceData -Force | Out-Null
}

Write-Step "Actualizando MCP config de Antigravity"
$primaryMcp = Join-Path $env:USERPROFILE ".gemini\antigravity\mcp_config.json"
$projectMcp = Join-Path $WorkspacePath "mcp_config.json"
Update-McpConfigFile -ConfigPath $primaryMcp -FilesystemRoot $workspaceData
Update-McpConfigFile -ConfigPath $projectMcp -FilesystemRoot $workspaceData

if ($SkipVm) {
    Write-Host "[done] Configuracion de Antigravity + Vertex completa (sin crear VM)." -ForegroundColor Green
    exit 0
}

Write-Step "Reservando IP estatica"
$addressName = "$InstanceName-ip"
$addressResult = Invoke-GcloudCapture -CommandArgs @("compute", "addresses", "describe", $addressName, "--region", $Region, "--format=value(address)")
$address = if ($addressResult.ExitCode -eq 0) { $addressResult.Output.Trim() } else { "" }
if (-not $address) {
    Invoke-Gcloud -CommandArgs @("compute", "addresses", "create", $addressName, "--region", $Region, "--quiet")
    for ($i = 0; $i -lt 10; $i++) {
        Start-Sleep -Seconds 2
        $addressResult = Invoke-GcloudCapture -CommandArgs @("compute", "addresses", "describe", $addressName, "--region", $Region, "--format=value(address)")
        $address = if ($addressResult.ExitCode -eq 0) { $addressResult.Output.Trim() } else { "" }
        if ($address) {
            break
        }
    }
    if (-not $address) {
        throw "No se pudo resolver la IP estatica '$addressName' despues de crearla."
    }
}

Write-Step "Asegurando firewall para conexion"
Ensure-FirewallRule -RuleName "antigravity-allow-ssh-iap" -RuleArgs @(
    "--allow=tcp:22",
    "--source-ranges=35.235.240.0/20",
    "--target-tags=antigravity",
    "--description=Allow SSH through IAP"
)
Ensure-FirewallRule -RuleName "antigravity-allow-devports" -RuleArgs @(
    "--allow=tcp:3000,tcp:4173,tcp:5173,tcp:8080,tcp:8888",
    "--source-ranges=0.0.0.0/0",
    "--target-tags=antigravity",
    "--description=Expose common dev ports for Antigravity remote usage"
)

$existsResult = Invoke-GcloudCapture -CommandArgs @("compute", "instances", "describe", $InstanceName, "--zone", $Zone, "--format=value(name)")
$exists = if ($existsResult.ExitCode -eq 0) { $existsResult.Output.Trim() } else { "" }
if ($exists -eq $InstanceName) {
    Write-Host "[done] La VM '$InstanceName' ya existe. No se recreo." -ForegroundColor Green
} else {
    Write-Step "Seleccionando machine type de maximo perfil disponible en $Zone"
    $candidates = Get-CandidateMachineTypes -ZoneName $Zone -PreferredMachineType $MachineType
    if (-not $candidates -or $candidates.Count -eq 0) {
        throw "No se encontraron machine types candidatos."
    }

    $created = $false
    $selectedType = ""
    foreach ($candidate in $candidates) {
        Write-Host "Intentando crear VM con machine type: $candidate" -ForegroundColor DarkCyan
        $createVmArgs = @(
            "compute", "instances", "create", $InstanceName,
            "--zone=$Zone",
            "--machine-type=$candidate",
            "--boot-disk-type=$BootDiskType",
            "--boot-disk-size=${BootDiskGb}GB",
            "--image-family=ubuntu-2204-lts",
            "--image-project=ubuntu-os-cloud",
            "--network-tier=PREMIUM",
            "--address=$address",
            "--tags=antigravity",
            "--scopes=cloud-platform",
            "--metadata=enable-oslogin=TRUE",
            "--quiet"
        )
        $createVmResult = Invoke-GcloudCapture -CommandArgs $createVmArgs
        if ($createVmResult.ExitCode -eq 0) {
            $created = $true
            $selectedType = $candidate
            break
        } else {
            $reason = (($createVmResult.Output -split "`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -First 2) -join " | ")
            if (-not $reason) {
                $reason = "quota/policy/capacidad"
            }
            Write-Host "No se pudo crear con $candidate. Probando siguiente... Detalle: $reason" -ForegroundColor Yellow
        }
    }

    if (-not $created) {
        throw "No se pudo crear la VM con los perfiles altos. Revisa cuotas/limites y define -MachineType manualmente."
    }

    Write-Host "[done] VM creada: $InstanceName ($selectedType)" -ForegroundColor Green
}

$resolvedDataDiskName = if ([string]::IsNullOrWhiteSpace($DataDiskName)) { "$InstanceName-data" } else { $DataDiskName }
if ($DataDiskGb -gt 0) {
    $dataDisk = Invoke-GcloudCapture -CommandArgs @("compute", "disks", "describe", $resolvedDataDiskName, "--zone", $Zone, "--format=value(name)")
    if ($dataDisk.ExitCode -ne 0) {
        Write-Step "Creando disco adicional de datos (${DataDiskGb}GB, $DataDiskType)"
        $createDiskResult = Invoke-GcloudCapture -CommandArgs @(
            "compute", "disks", "create", $resolvedDataDiskName,
            "--zone=$Zone",
            "--type=$DataDiskType",
            "--size=${DataDiskGb}GB",
            "--quiet"
        )
        if ($createDiskResult.ExitCode -ne 0) {
            $diskReason = (($createDiskResult.Output -split "`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -First 2) -join " | ")
            Write-Host "[warn] No se pudo crear disco de datos '$resolvedDataDiskName': $diskReason" -ForegroundColor Yellow
        }
    }

    $attachedDisks = Invoke-GcloudCapture -CommandArgs @("compute", "instances", "describe", $InstanceName, "--zone", $Zone, "--format=value(disks[].source.basename())")
    $isAttached = $false
    if ($attachedDisks.ExitCode -eq 0) {
        $attachedNames = $attachedDisks.Output -split "`n"
        $isAttached = $attachedNames -contains $resolvedDataDiskName
    }

    if (-not $isAttached) {
        Write-Step "Adjuntando disco adicional '$resolvedDataDiskName'"
        $attachResult = Invoke-GcloudCapture -CommandArgs @(
            "compute", "instances", "attach-disk", $InstanceName,
            "--zone=$Zone",
            "--disk=$resolvedDataDiskName",
            "--device-name=data",
            "--quiet"
        )
        if ($attachResult.ExitCode -ne 0) {
            $attachReason = (($attachResult.Output -split "`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -First 2) -join " | ")
            Write-Host "[warn] No se pudo adjuntar disco '$resolvedDataDiskName': $attachReason" -ForegroundColor Yellow
        }
    }
}

$natResult = Invoke-GcloudCapture -CommandArgs @("compute", "instances", "describe", $InstanceName, "--zone", $Zone, "--format=value(networkInterfaces[0].accessConfigs[0].natIP)")
$natIp = if ($natResult.ExitCode -eq 0) { $natResult.Output.Trim() } else { "" }
Write-Host ""
Write-Host "==== RESUMEN ====" -ForegroundColor Green
Write-Host "Project: $ProjectId"
Write-Host "Region:  $Region"
Write-Host "Zone:    $Zone"
Write-Host "VM:      $InstanceName"
Write-Host "IP:      $natIp"
Write-Host "Boot:    ${BootDiskGb}GB $BootDiskType"
if ($DataDiskGb -gt 0) {
    Write-Host "Data:    ${DataDiskGb}GB $DataDiskType ($resolvedDataDiskName)"
}
Write-Host "MCP:     $primaryMcp"
Write-Host ""
Write-Host "Conecta por SSH con:" -ForegroundColor Yellow
Write-Host "  `"$script:GcloudPath`" compute ssh $InstanceName --zone $Zone"
Write-Host ""
Write-Host "Reinicia Antigravity para que tome la nueva configuracion MCP/env vars." -ForegroundColor Yellow

