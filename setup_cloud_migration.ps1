# Setup Script for PC 1 Migration
$PROJECT_ROOT = "C:\Users\Lenovo\Antigravity_Cloud_Project"
$REPO_NAME = "antigravity-unified-cloud"

Write-Host "Initializing unified repository at $PROJECT_ROOT..."
Set-Location $PROJECT_ROOT

# Check if git is initialized
if (-not (Test-Path ".git")) {
    git init
    git branch -m main
} else {
    Write-Host "Git already initialized."
}

# Check for gcloud
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: gcloud CLI not found. Please install Google Cloud SDK." -ForegroundColor Red
    exit 1
}

# Create Cloud Repo (try/catch to avoid error if exists)
Write-Host "Creating Cloud Source Repository: $REPO_NAME"
try {
    # This might require interactive login if not authenticated
    cmd /c "gcloud source repos create $REPO_NAME --project=$(gcloud config get-value project)" 2>$null
} catch {
    Write-Host "Repo might already exist or auth required. Proceeding..."
}

# Add Remote
$PROJECT_ID = (gcloud config get-value project)
if (-not $PROJECT_ID) {
    Write-Host "WARNING: No Google Cloud Project selected. Run 'gcloud config set project YOUR_PROJECT_ID'" -ForegroundColor Yellow
} else {
    $REPO_URL = "https://source.developers.google.com/p/$PROJECT_ID/r/$REPO_NAME"
    
    # Check if remote exists
    cmd /c "git remote remove google" 2>$null
    git remote add google $REPO_URL
    
    # Commit & Push
    git add .
    git commit -m "Initial setup from PC 1 Architect"
    
    Write-Host "Pushing to Cloud..."
    git push google main

    Write-Host "---------------------------------------------------"
    Write-Host "MIGRATION SETUP COMPLETE on PC 1"
    Write-Host "Repository URL for PC 2: $REPO_URL"
    Write-Host "---------------------------------------------------"
    Write-Host "INSTRUCTIONS FOR PC 2:"
    Write-Host "1. Clone this repo: git clone $REPO_URL"
    Write-Host "2. Checkout branch: git checkout -b pc2-legacy"
    Write-Host "3. Copy your local files into the folder."
    Write-Host "4. Commit and push: git push origin pc2-legacy"
    Write-Host "---------------------------------------------------"
}
