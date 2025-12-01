# Project Structure

```
c:\Users\lokeshwar.reddy\project\
│
├── 📁 config/
│   ├── __init__.py
│   └── config.py                    # Configuration management & settings
│
├── 📁 src/
│   ├── __init__.py
│   ├── broker.py                    # Zerodha Kite API integration
│   ├── order_manager.py             # Order execution & position tracking
│   ├── risk_manager.py              # Risk & position management
│   │
│   ├── 📁 data/
│   │   ├── __init__.py
│   │   └── data_handler.py          # Historical & live data fetching
│   │
│   ├── 📁 strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py         # Base strategy framework
│   │   └── technical_strategies.py  # MA, RSI, MACD, BB, Combined strategies
│   │
│   ├── 📁 backtesting/
│   │   ├── __init__.py
│   │   └── backtester.py            # Backtesting engine with metrics
│   │
│   └── 📁 utils/
│       ├── __init__.py
│       ├── logger.py                # Logging utility
│       └── helpers.py               # Helper functions
│
├── 📁 data/
│   ├── 📁 historical/               # Historical data storage (CSV/Pickle)
│   └── (trading.db)                 # SQLite database (created at runtime)
│
├── 📁 logs/
│   └── (trading_YYYYMMDD.log)       # Daily log files (created at runtime)
│
├── 📁 tests/
│   └── (test files)                 # Unit tests (to be added)
│
├── 📄 main.py                       # Main application with interactive menu
├── 📄 examples.py                   # Usage examples & demonstrations
├── 📄 test_setup.py                 # Installation verification tests
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env.template                 # Environment variables template
├── 📄 .gitignore                    # Git ignore rules
│
├── 📄 README.md                     # Complete documentation
├── 📄 SETUP.md                      # Quick setup guide
├── 📄 PROJECT_SUMMARY.md            # Project overview & summary
└── 📄 QUICK_REFERENCE.md            # Quick command reference

```

## 📦 Core Components

### 1. Configuration Layer
- **config/config.py**: Centralized configuration management
- **.env**: Environment variables (API keys, trading parameters)

### 2. Data Layer
- **src/data/data_handler.py**: Fetches data from multiple sources
  - Yahoo Finance (yfinance)
  - NSE Python (nsepy)
  - Zerodha Kite (for live data)

### 3. Strategy Layer
- **src/strategies/base_strategy.py**: Abstract base class for strategies
- **src/strategies/technical_strategies.py**: 
  - Moving Average Crossover
  - RSI Strategy
  - MACD Strategy
  - Bollinger Bands
  - Combined Strategy

### 4. Execution Layer
- **src/broker.py**: Zerodha Kite API wrapper
- **src/order_manager.py**: Order placement & tracking
- **src/risk_manager.py**: Risk controls & position sizing

### 5. Analysis Layer
- **src/backtesting/backtester.py**: 
  - Performance metrics
  - Trade logging
  - Visualization

### 6. Utility Layer
- **src/utils/logger.py**: Colored console & file logging
- **src/utils/helpers.py**: Common utility functions

## 🎯 Entry Points

### Main Application
```bash
python main.py
```
Interactive menu for:
- Running backtests
- Comparing strategies
- Paper trading
- Live trading

### Examples
```bash
python examples.py
```
Demonstrations of:
- Fetching data
- Creating strategies
- Running backtests
- Risk management
- Scanning stocks

### Setup Test
```bash
python test_setup.py
```
Verifies:
- Package installation
- Configuration
- Data fetching
- Strategy execution
- Backtesting

## 📊 Data Flow

```
1. Data Fetching
   ↓
   data_handler.py → Yahoo Finance / NSEpy / Kite API
   ↓
   Historical OHLCV Data (DataFrame)

2. Strategy Processing
   ↓
   base_strategy.py → calculate_indicators()
   ↓
   technical_strategies.py → generate_signals()
   ↓
   Trading Signals (1=Buy, -1=Sell, 0=Hold)

3. Risk Management
   ↓
   risk_manager.py → calculate_position_size()
   ↓
   Position Size, Stop Loss, Take Profit

4. Order Execution
   ↓
   order_manager.py → place_order()
   ↓
   broker.py (Paper or Live)
   ↓
   Order Confirmation

5. Position Tracking
   ↓
   order_manager.py → track positions
   ↓
   P&L Calculation & Logging
```

## 🔄 Workflow

### Backtesting Workflow
```
User Input (Symbol, Strategy)
↓
Fetch Historical Data (data_handler)
↓
Calculate Indicators (strategy)
↓
Generate Signals (strategy)
↓
Simulate Trading (backtester)
↓
Calculate Metrics (backtester)
↓
Display Results & Charts
```

### Paper Trading Workflow
```
User Input (Symbols, Strategy)
↓
Fetch Latest Data (data_handler)
↓
Generate Signals (strategy)
↓
Calculate Risk (risk_manager)
↓
Place Orders (order_manager - paper mode)
↓
Track Positions & P&L
↓
Save Results & Logs
```

### Live Trading Workflow
```
Authenticate (broker.py)
↓
Fetch Real-time Data (Kite API)
↓
Generate Signals (strategy)
↓
Validate Risk (risk_manager)
↓
Place Live Orders (broker.py)
↓
Monitor Positions (order_manager)
↓
Execute Stop Loss / Take Profit
↓
Log Trades & P&L
```

## 📈 Strategy Architecture

```
BaseStrategy (Abstract)
├── calculate_indicators() → Add technical indicators
├── generate_signals() → Generate buy/sell signals
├── backtest() → Simple backtest
└── get_current_signal() → Latest signal

↓ Inherited by ↓

Technical Strategies:
├── MovingAverageCrossover
├── RSIStrategy
├── MACDStrategy
├── BollingerBandsStrategy
└── CombinedStrategy
```

## 🛡️ Risk Management Flow

```
Entry Price + Stop Loss
↓
Risk Manager
├── Calculate Position Size
├── Validate Order
├── Check Daily Limits
└── Check Max Positions
↓
Order Manager
├── Place Order
├── Track Position
└── Monitor Stop Loss/Take Profit
```

## 📁 File Sizes (Approximate)

| File | Lines | Purpose |
|------|-------|---------|
| broker.py | 250 | Zerodha API integration |
| data_handler.py | 200 | Data fetching |
| base_strategy.py | 130 | Strategy framework |
| technical_strategies.py | 250 | Strategy implementations |
| backtester.py | 280 | Backtesting engine |
| risk_manager.py | 180 | Risk management |
| order_manager.py | 300 | Order execution |
| main.py | 300 | Main application |
| examples.py | 270 | Usage examples |

**Total: ~2,200 lines of well-documented Python code**

## 🎨 Key Features

✅ **5 Trading Strategies** ready to use
✅ **Paper Trading** for safe testing
✅ **Live Trading** with Zerodha API
✅ **Comprehensive Backtesting** with metrics
✅ **Risk Management** with position sizing
✅ **Multiple Data Sources** (Yahoo, NSE, Kite)
✅ **Logging & Monitoring** for all activities
✅ **Visualization** of results
✅ **Modular Design** for easy extension

## 🔌 Dependencies

**Core Libraries:**
- kiteconnect - Zerodha API
- pandas - Data manipulation
- numpy - Numerical operations
- yfinance - Market data
- nsepy - NSE data

**Analysis:**
- pandas-ta - Technical indicators
- matplotlib - Visualization
- backtrader - Backtesting support

**Utilities:**
- python-dotenv - Configuration
- colorlog - Colored logging
- pytz - Timezone handling

## 🎓 Learning Path

1. **Start Here**: `README.md`
2. **Quick Setup**: `SETUP.md`
3. **Try Examples**: `examples.py`
4. **Run Backtests**: `main.py` → Option 1
5. **Paper Trade**: `main.py` → Option 3
6. **Study Code**: Read strategy implementations
7. **Customize**: Create your own strategies
8. **Go Live**: After thorough testing

## 🔐 Security Notes

- `.env` file contains sensitive data (ignored by git)
- API credentials never committed
- Access tokens stored locally
- Paper trading by default

## 📝 Notes

- All prices in INR (₹)
- Market hours: 9:15 AM - 3:30 PM IST
- Data updated daily
- Logs rotated daily
- Supports NSE & BSE stocks

---

**Built for Indian stock market traders using Zerodha** 🇮🇳📈
