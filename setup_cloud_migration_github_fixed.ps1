# Setup Cloud Migration (GitHub Fallback) - FIXED PATH
$PROJECT_ROOT = "C:\Users\Lenovo\Antigravity_Cloud_Project"
$REPO_NAME = "antigravity-unified-cloud"
$GH_PATH = "$env:USERPROFILE\gh\bin\gh.exe"

# Add Loop to PATH just in case
$env:Path += ";$env:USERPROFILE\gh\bin"

Write-Host "Authenticating with GitHub..."
# Open browser login
Start-Process -FilePath $GH_PATH -ArgumentList "auth login -w" -NoNewWindow -Wait

Write-Host "Verifying Login..."
& $GH_PATH auth status

if ($LASTEXITCODE -ne 0) {
    Write-Host "Login failed or not completed. Please try running 'C:\Users\Lenovo\gh\bin\gh.exe auth login -w' manually." -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 2

Set-Location $PROJECT_ROOT

# Initialize remote repo on GitHub (Private)
Write-Host "Creating Private GitHub Repository..."
try {
    # Check if repo exists
    & $GH_PATH repo view $REPO_NAME >$null 2>&1
    if ($?) {
        Write-Host "Repo already exists."
    } else {
        & $GH_PATH repo create $REPO_NAME --private --source=. --remote=google
    }
} catch {
    Write-Host "Error checking/creating repo. It might already exist."
}

# Ensure remote is set
$USERNAME = & $GH_PATH api user --jq ".login"
$REPO_URL = "https://github.com/$USERNAME/$REPO_NAME.git"

if (-not (git remote get-url google 2>$null)) {
    git remote add google $REPO_URL
} else {
    git remote set-url google $REPO_URL
}

# Push
git push -u google main

Write-Host "---------------------------------------------------"
Write-Host "MIGRATION SETUP COMPLETE (Via GitHub)"
Write-Host "Repository URL for PC 2: $REPO_URL"
Write-Host "---------------------------------------------------"
Write-Host "INSTRUCTIONS FOR PC 2:"
Write-Host "1. Install GitHub CLI or git"
Write-Host "2. Clone: git clone $REPO_URL"
Write-Host "3. Checkout branch: git checkout -b pc2-legacy"
Write-Host "4. Push: git push origin pc2-legacy"
