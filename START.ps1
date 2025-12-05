# Trading System Launcher for Windows
# Double-click this file to start

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "ALGORITHMIC TRADING SYSTEM" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (Test-Path "venv\Scripts\python.exe") {
    $pythonCmd = "venv\Scripts\python.exe"
    Write-Host "✓ Using virtual environment" -ForegroundColor Green
} else {
    $pythonCmd = "python"
    Write-Host "⚠ Virtual environment not found, using system Python" -ForegroundColor Yellow
}

Write-Host ""

# Run the launcher
& $pythonCmd start.py

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
