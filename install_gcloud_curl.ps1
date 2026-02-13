$installerUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$installerPath = "$env:TEMP\GoogleCloudSDKInstaller.exe"
$installDir = "$env:USERPROFILE\GoogleCloudSDK"

Write-Host "Downloading Google Cloud SDK Installer using curl..."
Start-Process curl -ArgumentList "-L", "-o", $installerPath, $installerUrl -Wait

if (-not (Test-Path $installerPath)) {
    Write-Host "Installer download failed."
    exit 1
}

Write-Host "Running Installer Silently (this may take a few minutes)..."
Start-Process -FilePath $installerPath -ArgumentList "/S", "/D=$installDir", "/allusers" -Wait

# Update path manually for current session
$env:Path += ";$installDir\google-cloud-sdk\bin;$env:ProgramFiles\Google\Cloud SDK\google-cloud-sdk\bin;$env:ProgramFiles (x86)\Google\Cloud SDK\google-cloud-sdk\bin"

Write-Host "Verifying installation..."
try {
    gcloud --version
    Write-Host "Google Cloud SDK Installed Successfully!"
} catch {
    Write-Host "gcloud command not found immediately. Please restart your terminal."
}
