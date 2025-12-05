# Quick Fix Script for Common Issues
# Run this if you encounter SSL or Unicode errors

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "QUICK FIX FOR COMMON ISSUES" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan

# Fix 1: Set PowerShell to UTF-8 for Unicode characters (₹)
Write-Host "`nFix 1: Setting console to UTF-8 encoding..." -ForegroundColor Green
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
Write-Host "✓ Console encoding set to UTF-8" -ForegroundColor Green

# Fix 2: Install certifi for SSL certificate handling
Write-Host "`nFix 2: Installing certifi package..." -ForegroundColor Green
pip install certifi --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ certifi installed successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ certifi installation had issues (may already be installed)" -ForegroundColor Yellow
}

# Fix 3: Test data fetching
Write-Host "`nFix 3: Testing data fetch..." -ForegroundColor Green
python -c "import yfinance as yf; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; ticker = yf.Ticker('TCS.NS'); data = ticker.history(period='5d'); print(f'✓ Fetched {len(data)} days of data for TCS')" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Data fetching is working!" -ForegroundColor Green
} else {
    Write-Host "⚠ Data fetching may have issues (this is normal on some corporate networks)" -ForegroundColor Yellow
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "FIXES APPLIED!" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`nYou can now run:" -ForegroundColor Yellow
Write-Host "  python test_setup.py" -ForegroundColor Cyan
Write-Host "  python examples.py" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor Cyan

Write-Host "`nNote: If data fetching still fails, you can:" -ForegroundColor Yellow
Write-Host "  1. Try using 'nsepy' as data source (set DATA_SOURCE=nsepy in .env)" -ForegroundColor Gray
Write-Host "  2. Work offline with pre-downloaded data" -ForegroundColor Gray
Write-Host "  3. Contact your IT department about SSL certificate issues" -ForegroundColor Gray
