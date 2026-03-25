# cframe Windows installer
$ErrorActionPreference = "Stop"

$InstallBin = "$env:LOCALAPPDATA\cframe\bin"
$InstallData = "$env:APPDATA\cframe"

Write-Host "Installing cframe..."

# Create directories
New-Item -ItemType Directory -Force -Path $InstallBin | Out-Null
New-Item -ItemType Directory -Force -Path $InstallData | Out-Null

# Copy script
Copy-Item "cli\cframe.py" -Destination "$InstallBin\cframe.py" -Force

# Create batch wrapper
@"
@echo off
python "%~dp0cframe.py" %*
"@ | Set-Content "$InstallBin\cframe.bat"

# Copy templates (remove old first for clean install)
if (Test-Path "$InstallData\templates") {
    Remove-Item -Recurse -Force "$InstallData\templates"
}
Copy-Item -Recurse "templates" -Destination "$InstallData\templates"

Write-Host "Installed to:"
Write-Host "  $InstallBin\cframe.bat"
Write-Host "  $InstallData\templates\"

# Check if cframe is findable after install
if (-not (Get-Command cframe -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "Note: cframe is not in your PATH. Add it permanently:"
    Write-Host "  [Environment]::SetEnvironmentVariable('PATH', `"$InstallBin;`$env:PATH`", 'User')"
    Write-Host ""
    Write-Host "Or add via System Properties > Environment Variables"
}
