add-type -AssemblyName System.Windows.Forms
$ghParam = @{
    FilePath = "$env:USERPROFILE\gh\bin\gh.exe"
    ArgumentList = "auth login -p https -w"
    RedirectStandardOutput = "gh_output.txt"
    RedirectStandardError = "gh_error.txt"
    UseShellExecute = $false
    WindowStyle = "Hidden"
}

$p = Start-Process @ghParam -PassThru

Write-Host "Waiting for Auth Code..."
$code = ""
$startTime = Get-Date

do {
    Start-Sleep -Seconds 1
    if (Test-Path "gh_output.txt") {
        $content = Get-Content "gh_output.txt" -Raw
        if ($content -match "([A-Z0-9]{4}-[A-Z0-9]{4})") {
            $code = $matches[1]
            break
        }
    }
    if ((Get-Date) - $startTime -gt (New-TimeSpan -Seconds 30)) {
        Write-Host "Timeout waiting for code."
        Stop-Process $p
        exit 1
    }
} while ($true)

Write-Host "Code found: $code"

# Open Browser
Start-Process brave "https://github.com/login/device"

# Wait for browser to load
Start-Sleep -Seconds 8

# Type Code
Write-Host "Typing code..."
[System.Windows.Forms.SendKeys]::SendWait($code)
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

# Wait for next page "Authorize"
Start-Sleep -Seconds 3

# Try to Authorize (Tab to button?) usually it's the primary button.
# Let's try pressing Enter again.
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

Write-Host "Automation sequence finished. Waiting for auth completion..."

# Wait for GH to finish
$p.WaitForExit()
Write-Host "GitHub CLI Authenticated!"
