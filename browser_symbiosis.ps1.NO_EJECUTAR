# browser_symbiosis.ps1 - PowerShell Browser Orchestrator (Ultralight Edition)
# Connects to Brave running with --remote-debugging-port=9222
# Uses System.Windows.Forms for "Human Mimicry" typing

Add-Type -AssemblyName System.Windows.Forms

$DebugPort = "9222"
$BaseUrl = "http://127.0.0.1:$DebugPort"

function Get-BrowserVersion {
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl/json/version" -ErrorAction Stop
        return $response
    } catch {
        return $null
    }
}

function Get-Tabs {
    try {
        $tabs = Invoke-RestMethod -Uri "$BaseUrl/json/list" -ErrorAction Stop
        return $tabs | Where-Object { $_.type -eq 'page' }
    } catch {
        return @()
    }
}

function Activate-Tab {
    param([string]$TabId)
    try {
        Invoke-RestMethod -Uri "$BaseUrl/json/activate/$TabId" -Method Post -ErrorAction Stop
        Write-Host "Activated tab: $TabId" -ForegroundColor Green
        Start-Sleep -Milliseconds 500 # Wait for window focus
        return $true
    } catch {
        Write-Host "Failed to activate tab." -ForegroundColor Red
        return $false
    }
}

function Open-Tab {
    param([string]$Url)
    try {
        $tab = Invoke-RestMethod -Uri "$BaseUrl/json/new?$Url" -Method Put -ErrorAction Stop
        Write-Host "Opened new tab: $Url" -ForegroundColor Green
        return $tab
    } catch {
        Write-Host "Failed to open tab." -ForegroundColor Red
    }
}

function Inject-Text {
    param([string]$Text)
    Write-Host "KEYBOARD: Mimicking human typing..." -ForegroundColor Cyan
    $chars = $Text.ToCharArray()
    foreach ($char in $chars) {
        $strChar = "$char"
        if ($strChar -match "[+\^%~(){}]") { $strChar = "{$strChar}" }
        [System.Windows.Forms.SendKeys]::SendWait($strChar)
        Start-Sleep -Milliseconds (Get-Random -Minimum 10 -Maximum 50)
    }
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
}

function Find-Best-Tool {
    param($TaskType)
    $tabs = Get-Tabs
    
    foreach ($tab in $tabs) {
        $url = $tab.url
        if ($TaskType -eq 'CODING' -and $url -match 'claude.ai') { return @{Tab=$tab; Name='Claude Pro'} }
        if ($TaskType -eq 'DATA' -and $url -match 'chatgpt.com') { return @{Tab=$tab; Name='ChatGPT Plus'} }
        if ($TaskType -eq 'RESEARCH' -and ($url -match 'notebooklm' -or $url -match 'gemini.google')) { return @{Tab=$tab; Name='Gemini/NotebookLM'} }
        if ($TaskType -eq 'DEPLOY' -and ($url -match 'replit' -or $url -match 'idx.google')) { return @{Tab=$tab; Name='Replit/IDX'} }
    }
    return $null
}

# --- Main Interaction Loop ---

Write-Host "CONNECTING to Brave Browser on port $DebugPort..." -ForegroundColor Cyan

$version = Get-BrowserVersion
if (-not $version) {
    Write-Host "ERROR: Could not connect to Brave!" -ForegroundColor Red
    Write-Host "ACTION REQUIRED: Please close all Brave instances and run:" -ForegroundColor Yellow
    Write-Host "brave.exe --remote-debugging-port=9222" -ForegroundColor White
    exit
}

Write-Host "CONNECTED to $($version.Browser)" -ForegroundColor Green
$tabs = Get-Tabs
Write-Host "Found $($tabs.Count) active tabs." -ForegroundColor Gray

foreach ($tab in $tabs) {
    Write-Host " - [$($tab.title)] ($($tab.url))"
}

# -- Orchestration logic passed via args --
if ($args.Count -ge 2) {
    $TaskType = $args[0]
    $Prompt = $args[1]
    
    Write-Host "`nEXECUTING Order: '$Prompt' (Type: $TaskType)" -ForegroundColor Cyan
    $tool = Find-Best-Tool -TaskType $TaskType

    if ($tool) {
        Write-Host "TARGET Acquired: $($tool.Name)" -ForegroundColor Green
        if (Activate-Tab -TabId $tool.Tab.id) {
             Inject-Text -Text $Prompt
             Write-Host "PAYLOAD delivered." -ForegroundColor Green
        }
    } else {
        Write-Host "WARNING: No specific tool found. Searching..." -ForegroundColor Yellow
        $searchUrl = "https://www.google.com/search?q=$([uri]::EscapeDataString($Prompt))"
        $newTab = Open-Tab -Url $searchUrl
    }
} else {
    Write-Host "`nReady for orders. Pass arguments to execute." -ForegroundColor Gray
}
