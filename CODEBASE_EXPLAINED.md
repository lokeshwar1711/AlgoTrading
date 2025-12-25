# AlgoTrading Codebase — What It Does (Complete Walkthrough)

This document explains what the codebase in this workspace does, how it is structured, and what actually happens at runtime when you run the scripts.

## 1) What this project is

This is a Python **algorithmic trading toolkit** for Indian equities.

It provides:
- A **CLI menu app** to:
  - backtest technical-indicator strategies on historical OHLCV data
  - compare strategies
  - run a basic “paper trading session” (simulated orders/positions)
- An **offline mode** (for corporate networks / no internet) that generates sample OHLCV data locally.
- Optional **Zerodha Kite Connect** authentication and a broker wrapper (Kite API integration exists, but the project’s main menu does not yet implement a full continuous live trading loop).

## 2) High-level data/control flow

The main pipeline is:

1. **Data**: Fetch historical OHLCV candles into a Pandas DataFrame.
2. **Indicators**: Strategy computes technical indicators (MA, RSI, MACD, Bollinger Bands).
3. **Signals**: Strategy creates a `signal` series:
   - `1` = BUY
   - `-1` = SELL
   - `0` = HOLD
4. **Execution**:
   - **Backtest**: Simulate trades across the historical series.
   - **Paper trading**: Create simulated orders and track positions + realized P&L.
5. **Outputs**:
   - Print summaries
   - Write logs
   - Save plots and CSV/JSON artifacts

## 3) Key entrypoints (what you run)

### A) Launcher
- `start.py`
  - Presents a menu:
    1. Offline mode → imports and runs `run_offline.py`
    2. Online mode → imports and runs `run_online.py`
    3. Offline tests → runs `test_offline.py`
    4. Online tests → runs `test_online.py`
    5. Authenticate Zerodha → imports and runs `authenticate.py`

### B) Online mode wrapper
- `run_online.py`
  - Prints “ONLINE MODE” banner.
  - Calls `main.main()`.

### C) Main CLI application
- `main.py`
  - `main()` validates config and shows a menu:
    1. Run Backtest (Single Strategy)
    2. Compare Multiple Strategies
    3. Paper Trading Session
    4. Live Trading (requires Zerodha API) — currently prints “coming soon”
    5. Exit

### D) Offline mode
- `run_offline.py`
  - Generates sample OHLCV data (random walk-ish) and provides a menu:
    1. Backtest a Strategy
    2. Compare Multiple Strategies
    3. Test Risk Management
    4. Generate Sample Data (save as CSV under `data/historical/`)
    5. Exit

## 4) Configuration (how settings are loaded)

- `config/config.py`
  - Loads environment variables via `python-dotenv` (`load_dotenv()`).
  - Exposes `config` singleton with settings.
  - Important settings:
    - `TRADING_MODE`: `paper` or `live`
    - `CAPITAL`: starting capital
    - `DATA_SOURCE`: `yfinance` or `nsepy`
    - `MAX_RISK_PER_TRADE`, `MAX_DAILY_LOSS`, `MAX_OPEN_POSITIONS`
    - directory paths: `data/`, `data/historical/`, `logs/`
  - `config.validate()`:
    - If `TRADING_MODE == live`, requires Kite key/secret.
    - Creates directories if missing.

## 5) Logging

- `src/utils/logger.py`
  - `get_logger(name)` configures:
    - Colored console logging via `colorlog`
    - A daily log file: `logs/trading_YYYYMMDD.log`
  - Note: On Windows it attempts to open `sys.stdout` with UTF-8 encoding.

## 6) Data fetching (market data)

- `src/data/data_handler.py`
  - `DataHandler.get_historical_data(symbol, start_date, end_date, interval)`
    - Uses `config.HISTORICAL_DATA_DAYS` if start_date not provided.
  - `yfinance` mode:
    - Auto-adds `.NS` suffix unless symbol already ends in `.NS` or `.BO`.
    - Uses `yfinance.Ticker(symbol).history(...)`.
    - Standardizes columns to lowercase and resets index into a `date` column.
  - `nsepy` mode:
    - Uses `nsepy.get_history(symbol=..., start=..., end=...)`.
    - Standardizes column names to lowercase (spaces → underscores) and resets index.
  - Extra helpers:
    - `get_multiple_stocks(symbols)` returns dict: symbol → dataframe
    - `save_data(df, symbol)` / `load_data(symbol, date)` work with `data/historical/`
    - `get_nifty_50_stocks()` and `get_bank_nifty_stocks()` return hard-coded symbol lists

### SSL behavior
The module globally disables SSL verification via:

```python
ssl._create_default_https_context = ssl._create_unverified_context
```

This is meant to help on corporate networks that intercept SSL, but it reduces TLS certificate verification.

## 7) Strategy framework (signals)

### Base interface
- `src/strategies/base_strategy.py`
  - Strategies implement:
    - `calculate_indicators(df)`
    - `generate_signals(df)` which must add a `signal` column (1, 0, -1)
  - `get_current_signal(df)` computes indicators + signals and returns the last signal.
  - There is also a `BaseStrategy.backtest()` method, but the project mainly uses the more detailed backtester in `src/backtesting/backtester.py`.

### Implemented strategies and their exact rules
- `src/strategies/technical_strategies.py`

1) **MovingAverageCrossover**
- Indicators:
  - SMA or EMA short/long: `ma_short`, `ma_long`
- Signals:
  - BUY when `ma_short > ma_long` AND previous bar had `ma_short <= ma_long` (crossover up)
  - SELL when `ma_short < ma_long` AND previous bar had `ma_short >= ma_long` (crossover down)

2) **RSIStrategy**
- Indicator:
  - RSI computed from rolling mean gains/losses
- Signals:
  - BUY when RSI crosses **above** `oversold` threshold (default 30)
  - SELL when RSI crosses **below** `overbought` threshold (default 70)

3) **MACDStrategy**
- Indicators:
  - MACD = EMA(fast) - EMA(slow)
  - signal line = EMA(MACD, signal_period)
- Signals:
  - BUY on MACD crossing above signal line
  - SELL on MACD crossing below signal line

4) **BollingerBandsStrategy**
- Indicators:
  - `bb_middle` = rolling mean
  - `bb_upper/lower` = middle ± std_dev * rolling std
- Signals (as written):
  - BUY when close crosses above lower band
  - SELL when close crosses below upper band

5) **CombinedStrategy**
- Indicators computed: MA, RSI, MACD
- Signals (as written):
  - BUY when:
    - `ma_short > ma_long`
    - `rsi < 50`
    - `macd > macd_signal`
  - SELL when:
    - `ma_short < ma_long`
    - `rsi > 50`
    - `macd < macd_signal`

## 8) Backtesting engine (simulation + metrics)

- `src/backtesting/backtester.py`

### What it simulates
A simplified, single-position strategy execution:
- Holds at most **one open position at a time** (no scaling in/out, no multiple symbols).
- Trades are executed based only on strategy `signal` values.

### Trading rules used in simulation
- Maintains:
  - `capital` (cash)
  - `position` (units held)
  - `position_value` (entry value of the current position)
  - `portfolio_values` (tracked each candle)

At each candle:
- Portfolio value is computed as:
  - `portfolio_value = capital + position * close_price`
- BUY signal (`signal == 1`) and no position:
  - buys with 95% of current cash: `position = (capital * 0.95) / price`
  - reduces cash by position value
  - subtracts commission on the buy value
- SELL signal (`signal == -1`) and position open:
  - sells entire position
  - subtracts commission on the sell value
  - realized P&L computed relative to entry `position_value`

If a position is still open at the end, it force-sells on the final close.

### Metrics computed
- Total return (%)
- Trade counts: total buys, winning sells, losing sells, win rate
- Average win / average loss (from sell trades’ P&L)
- Max drawdown: min drawdown from portfolio equity curve
- Sharpe ratio:
  - uses portfolio daily returns
  - assumes 252 trading days
  - assumes 5% annual risk-free rate

### Outputs
- `print_summary()` prints metrics.
- `plot_results(df, save_path)` plots:
  1) close price + buy/sell markers
  2) portfolio value curve
  3) drawdown curve
- `get_trade_log()` returns trades as a DataFrame.

## 9) Paper trading execution + risk controls

### Risk manager
- `src/risk_manager.py`

What it tracks:
- `capital` (starting capital; updated only if you call `update_capital()`)
- `daily_pnl` (realized P&L from closed paper positions)
- `open_positions` count

Core calculations:
- Stop loss (percentage): `entry * (1 - pct/100)`
- Position sizing:
  - `risk_amount = capital * (risk_percentage/100)`
  - `qty = int(risk_amount / abs(entry - stop))`
- Take profit:
  - `take_profit = entry + abs(entry - stop) * reward_ratio`

Order validation (`validate_order`):
- cannot exceed max open positions
- cannot exceed daily loss limit
- max order value is 30% of capital
- min order value is ₹500

### Order manager
- `src/order_manager.py`

In paper mode:
- BUY:
  - creates a `Position` object and stores it in `positions[symbol]`
  - increments `RiskManager.open_positions`
- SELL:
  - closes the position
  - computes realized P&L
  - updates `RiskManager.daily_pnl`
  - decrements open positions
  - moves the position to `closed_positions`

It also supports:
- `check_stop_loss_take_profit(current_prices)`
  - if current price hits SL/TP, it triggers a SELL
  - note: the main CLI does not run a continuous price update loop; you would need a scheduler/loop that updates `current_prices` repeatedly.
- `save_positions(filepath)` writes open/closed positions and orders to JSON.

## 10) Zerodha Kite integration

### Authentication script
- `authenticate.py`
  - Uses `kiteconnect`:
    - opens browser for login URL
    - asks you to paste `request_token`
    - generates and saves `KITE_ACCESS_TOKEN` back into `.env`
    - verifies connection by calling `kite.profile()`
  - Note: Access tokens typically expire daily.

### Broker wrapper
- `src/broker.py`
  - Wraps KiteConnect API calls.
  - If `TRADING_MODE == paper`, `place_order()` returns a fake `PAPER_...` order id and logs it.
  - If `TRADING_MODE == live`, uses KiteConnect to place/modify/cancel orders and query account info.

### What is not fully implemented
- The main menu “Live Trading” option in `main.py` is not a full live-trading runtime.
- There is no continuous market-data stream loop (no websockets / no polling loop) that:
  - fetches live quotes,
  - recomputes signals on a schedule,
  - enforces SL/TP continuously,
  - and places actual live orders.

## 11) Offline mode (no internet)

- `run_offline.py`
  - Generates realistic-ish OHLCV using random returns and some noise.
  - Lets you backtest the same strategies on that generated dataset.
  - Can also generate and save a sample CSV under `data/historical/`.

- `test_offline.py`
  - A quick non-interactive sanity check that:
    - generates sample data
    - runs strategy signals
    - runs the backtester
    - runs risk sizing
    - places a paper order via OrderManager

## 12) Online tests and examples

- `examples.py`
  - Demonstrates:
    - fetching data
    - computing indicators
    - generating signals
    - running backtests
    - scanning a subset of Nifty stocks for signals

- `test_setup.py`
  - A setup verifier:
    - checks imports
    - checks config
    - tries yfinance data fetch
    - checks a strategy
    - checks the backtester
    - checks risk manager

- `test_online.py`
  - Similar to `test_setup.py` but oriented to “does the internet data fetch work?”

- `test_kite_api.py`
  - Validates Kite credentials are present and attempts a `kite.profile()` call if an access token exists.

## 13) Practical “what happens when I choose X?”

### Option: Backtest (main.py → option 1)
1. `config.validate()` ensures directories exist.
2. `DataHandler` fetches daily OHLCV via yfinance/nsepy.
3. Strategy computes indicators + signals.
4. `Backtester.run()` simulates trades across the time series.
5. It prints a summary.
6. It tries to save a plot to `logs/backtest_...png`.
7. It saves a trade log CSV to `data/trades_...csv`.

### Option: Compare strategies (main.py → option 2)
1. Fetch data once per strategy (because `run_backtest()` re-fetches each time).
2. Run backtest for each strategy.
3. Print a comparison table (return, win rate, trades, Sharpe, max drawdown).

### Option: Paper trading session (main.py → option 3)
This is a **single pass per symbol**, not a continuous session.
1. For each symbol:
   - Fetch daily data.
   - Compute latest signal.
2. If BUY signal:
   - Compute SL/TP and position sizing.
   - Place a paper BUY order (creates/open a Position).
3. If SELL signal and you have an open position:
   - Paper SELL order (closes position, realizes P&L).
4. Prints a summary.
5. Saves positions to JSON under `data/positions_YYYYMMDD.json`.

---

If you want, I can also generate a one-page “cheat sheet” version of this file with just the runtime flows and the most important functions/classes.
