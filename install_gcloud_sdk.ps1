$installerUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$installerPath = "$env:TEMP\GoogleCloudSDKInstaller.exe"
$installDir = "$env:USERPROFILE\GoogleCloudSDK"

Write-Host "Downloading Google Cloud SDK Installer..."
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

Write-Host "Running Installer Silently..."
Start-Process -FilePath $installerPath -ArgumentList "/S", "/D=$installDir" -Wait

Write-Host "Verifying installation..."
$env:Path += ";$installDir\google-cloud-sdk\bin"
gcloud --version

if ($LastExitCode -eq 0) {
    Write-Host "Google Cloud SDK Installed Successfully!"
} else {
    Write-Host "Installation might have failed or gcloud not found immediately."
}
