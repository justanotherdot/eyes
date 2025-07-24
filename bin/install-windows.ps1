#!/usr/bin/env pwsh
# Windows installation script for Eyes startup

param(
    [string]$EyesPath = ".\dist\eyes.exe",
    [int]$Interval = 20
)

$StartupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$BatchFile = "$StartupPath\eyes-startup.bat"

# Check if binary exists
if (-not (Test-Path $EyesPath)) {
    Write-Host "Error: eyes.exe not found at $EyesPath" -ForegroundColor Red
    Write-Host "Run './bin/build' first or specify correct path with -EyesPath" -ForegroundColor Yellow
    exit 1
}

# Get full path
$FullPath = (Resolve-Path $EyesPath).Path

# Create startup batch file
$BatchContent = @"
@echo off
REM Auto-generated startup script for Eyes
"$FullPath" --interval $Interval
"@

$BatchContent | Out-File -FilePath $BatchFile -Encoding ASCII

Write-Host "Eyes installed for Windows startup!" -ForegroundColor Green
Write-Host "Location: $BatchFile" -ForegroundColor Blue
Write-Host "It will start automatically on login with $Interval-minute intervals." -ForegroundColor Blue
Write-Host ""
Write-Host "To uninstall:" -ForegroundColor Yellow
Write-Host "  Remove-Item '$BatchFile'" -ForegroundColor Yellow