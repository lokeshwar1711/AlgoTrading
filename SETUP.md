# Quick Setup Guide

## Step 1: Create Virtual Environment

```powershell
# Navigate to project directory
cd c:\Users\lokeshwar.reddy\project

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

## Step 2: Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If `ta-lib` installation fails (it often does on Windows), you can skip it. The project uses `pandas-ta` as an alternative, which is already included.

To install ta-lib on Windows:
1. Download the wheel file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. Install using: `pip install TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl` (adjust for your Python version)

## Step 3: Configure Environment

```powershell
# Copy the template
copy .env.template .env

# Edit .env file with your settings
notepad .env
```

Required settings in `.env`:
```
KITE_API_KEY=your_api_key_here
KITE_API_SECRET=your_api_secret_here
TRADING_MODE=paper
CAPITAL=100000
```

## Step 4: Test Installation

```powershell
# Run examples to test
python examples.py
```

Select option 1 or 2 to verify everything is working.

## Step 5: Run Your First Backtest

```powershell
python main.py
```

Choose option 1, enter a stock symbol like `RELIANCE`, and select a strategy.

## Common Issues & Solutions

### Issue: Import errors
**Solution**: Make sure virtual environment is activated and all packages are installed
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "Could not resolve import" warnings
**Solution**: These are just IDE warnings. The code will run fine. You can ignore them or configure your Python interpreter in VS Code.

### Issue: No data fetched for stock
**Solution**: 
- Check internet connection
- Try with `.NS` suffix: `RELIANCE.NS`
- Try different data source in config (yfinance or nsepy)

### Issue: Zerodha API errors
**Solution**:
- Verify API credentials
- Generate a new access token
- Check if account is active

## Next Steps

1. **Paper Trade First**: Always test with paper trading before going live
2. **Backtest Thoroughly**: Test your strategies on at least 1 year of data
3. **Start Small**: When going live, start with small amounts
4. **Monitor Closely**: Watch your positions and logs carefully

## Getting Zerodha API Credentials

1. Go to https://kite.zerodha.com/
2. Login to your Zerodha account
3. Go to Console → API → Create New App
4. Fill in the details (app name, redirect URL, etc.)
5. Note down the API Key and API Secret
6. Add them to your `.env` file

## Running in Production

For live trading:
1. Change `TRADING_MODE=live` in `.env`
2. Generate access token first time
3. Run with proper monitoring
4. Keep logs directory monitored

## Support

Check the main README.md for detailed documentation.
