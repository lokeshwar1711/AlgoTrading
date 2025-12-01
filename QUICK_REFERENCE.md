# Quick Reference Guide

## Installation (One-time Setup)
```powershell
cd c:\Users\lokeshwar.reddy\project
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.template .env
# Edit .env with your settings
```

## Daily Usage

### Activate Virtual Environment
```powershell
cd c:\Users\lokeshwar.reddy\project
.\venv\Scripts\Activate.ps1
```

### Run Main Application
```powershell
python main.py
```

### Run Examples
```powershell
python examples.py
```

### Test Installation
```powershell
python test_setup.py
```

## Common Commands

### Backtest Single Stock
```powershell
python main.py
# Choose option 1
# Enter: RELIANCE (or any stock)
# Choose strategy: 1-5
```

### Compare All Strategies
```powershell
python main.py
# Choose option 2
# Enter: TCS (or any stock)
```

### Paper Trading
```powershell
python main.py
# Choose option 3
# Enter: RELIANCE,TCS,INFY (comma-separated)
# Choose strategy: 1-5
```

## Strategy Numbers
1. MA_Crossover (Moving Average)
2. RSI (Relative Strength Index)
3. MACD
4. BB (Bollinger Bands)
5. Combined (Multiple indicators)

## Popular Stocks to Test
```
# Large Cap
RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, ITC

# IT Sector
TCS, INFY, WIPRO, HCLTECH, TECHM

# Banking
HDFCBANK, ICICIBANK, SBIN, KOTAKBANK, AXISBANK

# Auto
MARUTI, TATAMOTORS, M&M, BAJAJ-AUTO

# Pharma
SUNPHARMA, DRREDDY, CIPLA, DIVISLAB
```

## File Locations

### Logs
```
logs/trading_YYYYMMDD.log
```

### Data
```
data/historical/SYMBOL_YYYYMMDD.csv
```

### Backtest Results
```
logs/backtest_SYMBOL_STRATEGY_YYYYMMDD.png
data/trades_SYMBOL_STRATEGY_YYYYMMDD.csv
```

### Positions
```
data/positions_YYYYMMDD.json
```

## Configuration (.env)

### Essential Settings
```
TRADING_MODE=paper          # paper or live
CAPITAL=100000              # Your capital
DATA_SOURCE=yfinance        # yfinance or nsepy
```

### Risk Settings
```
MAX_RISK_PER_TRADE=2        # % of capital per trade
MAX_DAILY_LOSS=5            # % max loss per day
MAX_OPEN_POSITIONS=5        # Max simultaneous positions
```

### Zerodha API (for live trading)
```
KITE_API_KEY=your_key
KITE_API_SECRET=your_secret
KITE_ACCESS_TOKEN=         # Generate on first use
```

## Quick Python Usage

### Fetch Data
```python
from src.data.data_handler import DataHandler

data = DataHandler()
df = data.get_historical_data('RELIANCE')
print(df.tail())
```

### Run Strategy
```python
from src.strategies.technical_strategies import RSIStrategy

strategy = RSIStrategy()
signal = strategy.get_current_signal(df)
# 1=Buy, -1=Sell, 0=Hold
```

### Backtest
```python
from src.backtesting.backtester import Backtester

backtester = Backtester(strategy, initial_capital=100000)
results = backtester.run(df)
backtester.print_summary()
```

### Risk Management
```python
from src.risk_manager import RiskManager

risk = RiskManager(capital=100000)
qty = risk.calculate_position_size(2500, 2450)  # entry, stop_loss
```

## Troubleshooting

### "Module not found"
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "No data fetched"
- Check internet
- Try symbol with .NS: `RELIANCE.NS`
- Change DATA_SOURCE in .env

### "Import errors in IDE"
- These are warnings, code will run
- Or: Select Python interpreter from venv

### "API connection failed"
- Check credentials in .env
- Generate new access token
- Verify Zerodha account

## Performance Metrics Explained

- **Total Return**: Overall profit/loss %
- **Win Rate**: % of profitable trades
- **Sharpe Ratio**: Risk-adjusted return (>1 is good)
- **Max Drawdown**: Largest loss from peak (lower is better)
- **Avg Win/Loss**: Average per winning/losing trade

## Best Practices

1. ✅ Always backtest first (1+ year data)
2. ✅ Use paper trading before live
3. ✅ Start with small capital
4. ✅ Set stop losses
5. ✅ Monitor regularly
6. ✅ Keep logs
7. ✅ Review performance weekly
8. ✅ Don't overtrade

## Risk Warnings

⚠️ Trading involves substantial risk
⚠️ Past performance ≠ future results
⚠️ Never risk more than you can lose
⚠️ This is for educational purposes
⚠️ Not financial advice

## Support Resources

- Project README: `README.md`
- Setup Guide: `SETUP.md`
- Project Summary: `PROJECT_SUMMARY.md`
- Logs: `logs/` directory
- Zerodha API: https://kite.trade/

## Quick Keyboard Shortcuts

When running applications:
- `Ctrl+C` - Stop/Exit
- Follow on-screen menus
- Enter numbers to select options

## Data Sources

### yfinance (Default)
- Free
- Reliable
- Easy to use
- Indian stocks: Add .NS suffix

### nsepy
- NSE official data
- Free
- Sometimes slower
- Indian stocks only

### Kite API (Live mode)
- Real-time data
- Requires API credentials
- Most accurate

## Updating the System

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Update packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade yfinance
```

## Getting Help

1. Check logs in `logs/` directory
2. Review error messages
3. Verify configuration in `.env`
4. Run `python test_setup.py`
5. Check internet connection

---

**Quick Start**: 
1. `.\venv\Scripts\Activate.ps1`
2. `python main.py`
3. Choose option, enter stock, select strategy
4. Review results

**That's it! Happy Trading! 🚀**
