$ErrorActionPreference = "Stop"

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$PROJECT_ROOT = "C:\Users\Lenovo\Antigravity_Cloud_Project"
$REPO_NAME = "antigravity-unified-cloud"

Write-Host "Checking Authentication..."
try {
    $accounts = gcloud auth list --format="value(account)" | Out-String
    if (-not $accounts -or $accounts.Trim() -eq "") {
        Write-Host "Authenticating... A browser window will open." -ForegroundColor Cyan
        cmd /c "gcloud auth login --quiet"
    } else {
        Write-Host "Authenticated as: $accounts"
    }
} catch {
    Write-Host "Failed to check authentication. Gcloud might not be in PATH or installed correctly."
    exit 1
}

Write-Host "Configuring Project..."
$currentProject = gcloud config get-value project 2>$null
if (-not $currentProject -or $currentProject -eq "(unset)") {
    $projects = gcloud projects list --format="value(projectId)" | Out-String
    $projList = $projects.Split("`n", [StringSplitOptions]::RemoveEmptyEntries) | ForEach-Object { $_.Trim() }
    
    if ($projList.Count -ge 1) {
        $selectedProject = $projList[0]
        Write-Host "Automatically selecting project: $selectedProject" -ForegroundColor Green
        cmd /c "gcloud config set project $selectedProject --quiet"
    } else {
        Write-Host "No Google Cloud Projects found. Please create one in Cloud Console first." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Using Project: $currentProject"
}

# Create Repo
Set-Location $PROJECT_ROOT
Write-Host "Creating Cloud Source Repository: $REPO_NAME"
cmd /c "gcloud source repos create $REPO_NAME --quiet" 2>$null

# Push
$projectId = gcloud config get-value project
$REPO_URL = "https://source.developers.google.com/p/$projectId/r/$REPO_NAME"

Write-Host "Pushing to: $REPO_URL"
git remote remove google 2>$null
git remote add google $REPO_URL
git push google main

Write-Host "SUCCESS! Migration Complete on PC 1."
