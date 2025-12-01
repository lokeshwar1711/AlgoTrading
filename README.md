# Algorithmic Trading System for Indian Markets

A comprehensive Python-based algorithmic trading system designed for Zerodha Kite API, focusing on Indian stock markets with support for options trading.

## 🚀 Features

- **Multiple Trading Strategies**
  - Moving Average Crossover (SMA/EMA)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Combined Multi-Indicator Strategy

- **Risk Management**
  - Position sizing based on risk percentage
  - Automatic stop-loss and take-profit
  - Maximum daily loss limits
  - Portfolio diversification controls

- **Backtesting Engine**
  - Comprehensive performance metrics
  - Win rate, Sharpe ratio, max drawdown
  - Visual charts and trade logs
  - Strategy comparison tools

- **Paper Trading**
  - Test strategies without real money
  - Real-time signal generation
  - Position tracking and P&L calculation

- **Live Trading** (Coming Soon)
  - Integration with Zerodha Kite API
  - Real-time order execution
  - Position monitoring

## 📋 Prerequisites

- Python 3.8 or higher
- Zerodha trading account (for live trading)
- Kite Connect API credentials

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```powershell
   cd c:\Users\lokeshwar.reddy\project
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```powershell
   cp .env.template .env
   ```
   
   Edit `.env` file and add your credentials:
   - Zerodha API Key and Secret (get from https://kite.zerodha.com/)
   - Adjust trading parameters as needed

## 📁 Project Structure

```
project/
├── config/
│   └── config.py              # Configuration management
├── src/
│   ├── broker.py              # Zerodha Kite API integration
│   ├── order_manager.py       # Order execution and tracking
│   ├── risk_manager.py        # Risk and position management
│   ├── data/
│   │   └── data_handler.py    # Data fetching from multiple sources
│   ├── strategies/
│   │   ├── base_strategy.py   # Base strategy class
│   │   └── technical_strategies.py  # Technical indicator strategies
│   ├── backtesting/
│   │   └── backtester.py      # Backtesting engine
│   └── utils/
│       └── logger.py          # Logging utility
├── data/                      # Historical data storage
├── logs/                      # Application logs
├── main.py                    # Main application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎯 Usage

### Running the Application

```powershell
python main.py
```

### 1. Backtest a Strategy

Test how a strategy would have performed on historical data:

```python
# Example: Backtest MA Crossover on RELIANCE
python main.py
# Select option 1
# Enter symbol: RELIANCE
# Select strategy: 1 (MA_Crossover)
```

### 2. Compare Multiple Strategies

Compare all strategies on a single stock:

```python
python main.py
# Select option 2
# Enter symbol: TCS
```

### 3. Paper Trading

Run strategies on current market data without real money:

```python
python main.py
# Select option 3
# Enter symbols: RELIANCE,TCS,INFY
# Select strategy: 5 (Combined)
```

### Using Individual Modules

#### Fetch Historical Data

```python
from src.data.data_handler import DataHandler

data_handler = DataHandler(data_source='yfinance')
df = data_handler.get_historical_data('RELIANCE', interval='1d')
print(df.head())
```

#### Run a Strategy

```python
from src.strategies.technical_strategies import MovingAverageCrossover

strategy = MovingAverageCrossover(short_window=20, long_window=50)
df = strategy.calculate_indicators(df)
df = strategy.generate_signals(df)
```

#### Backtest

```python
from src.backtesting.backtester import Backtester

backtester = Backtester(strategy, initial_capital=100000)
results = backtester.run(df)
backtester.print_summary()
backtester.plot_results(df)
```

## 📊 Available Strategies

### 1. Moving Average Crossover
- **Buy**: When short MA crosses above long MA
- **Sell**: When short MA crosses below long MA
- Parameters: `short_window`, `long_window`, `ma_type` (SMA/EMA)

### 2. RSI Strategy
- **Buy**: When RSI crosses above oversold level (default 30)
- **Sell**: When RSI crosses below overbought level (default 70)
- Parameters: `period`, `oversold`, `overbought`

### 3. MACD Strategy
- **Buy**: When MACD line crosses above signal line
- **Sell**: When MACD line crosses below signal line
- Parameters: `fast`, `slow`, `signal`

### 4. Bollinger Bands
- **Buy**: When price crosses above lower band
- **Sell**: When price crosses below upper band
- Parameters: `period`, `std_dev`

### 5. Combined Strategy
- Uses multiple indicators for confirmation
- More conservative but potentially more reliable

## 🔐 Zerodha API Setup

1. **Create a Kite Connect App**
   - Go to https://developers.kite.trade/
   - Create a new app
   - Note down API Key and API Secret

2. **Generate Access Token**
   ```python
   from src.broker import ZerodhaBroker
   
   broker = ZerodhaBroker()
   login_url = broker.get_login_url()
   print(f"Login URL: {login_url}")
   # After login, you'll get a request_token
   # Use it to generate access token
   ```

3. **Update .env file**
   - Add your API credentials
   - Set TRADING_MODE to 'live' for actual trading

## ⚠️ Risk Warning

**IMPORTANT**: 
- This is for educational purposes
- Always test strategies thoroughly with paper trading first
- Never risk more than you can afford to lose
- Past performance doesn't guarantee future results
- The developers are not responsible for any financial losses

## 📈 Performance Metrics

The backtester calculates:
- **Total Return**: Overall profit/loss percentage
- **Win Rate**: Percentage of profitable trades
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Average Win/Loss**: Average profit and loss per trade

## 🔧 Configuration

Edit `config/config.py` or `.env` to customize:
- Initial capital
- Risk per trade
- Maximum daily loss
- Maximum open positions
- Technical indicator periods
- Data sources

## 📝 Logging

Logs are saved in the `logs/` directory with daily rotation:
- Console output with colors
- File logging with full details
- Separate logs for each trading day

## 🤝 Contributing

Feel free to:
- Add new strategies
- Improve existing features
- Report bugs
- Suggest enhancements

## 📚 Resources

- [Zerodha Kite Connect API](https://kite.trade/)
- [Python for Finance](https://www.python.org/)
- [Technical Analysis Library](https://github.com/bukosabino/ta)
- [Backtrader Documentation](https://www.backtrader.com/)

## 🐛 Troubleshooting

### Import Errors
```powershell
pip install -r requirements.txt
```

### Data Fetching Issues
- Check internet connection
- Verify stock symbol format (NSE symbols)
- Try different data sources (yfinance vs nsepy)

### API Connection Issues
- Verify API credentials
- Check if access token is valid
- Ensure Zerodha account is active

## 📞 Support

For issues and questions:
- Check logs in `logs/` directory
- Review configuration in `.env`
- Ensure all dependencies are installed

## 📄 License

This project is for educational purposes. Use at your own risk.

---

**Happy Trading! 🚀📈**

*Remember: The best strategy is one that you understand and have tested thoroughly.*
