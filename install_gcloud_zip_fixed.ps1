$gcloudZipUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-463.0.0-windows-x86_64-bundled-python.zip"
$tempZipPath = "$env:TEMP\gcloud.zip"
$installDir = "$env:USERPROFILE\GoogleCloudSDK"

Write-Host "Downloading Google Cloud SDK (bundled python)..."
try {
    Invoke-WebRequest -Uri $gcloudZipUrl -OutFile $tempZipPath
} catch {
    Write-Host "Download failed: $_"
    exit 1
}

Write-Host "Extracting to $installDir..."
Expand-Archive -Path $tempZipPath -DestinationPath $installDir -Force

Write-Host "Installing silently using install.bat..."
Set-Location "$installDir\google-cloud-sdk"
.\install.bat --quiet --usage-reporting false --command-completion true --path-update true

Write-Host "Adding to PATH..."
$env:Path += ";$installDir\google-cloud-sdk\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, "User")

Write-Host "Verifying installation..."
gcloud --version

Write-Host "Installation COMPLETE."
