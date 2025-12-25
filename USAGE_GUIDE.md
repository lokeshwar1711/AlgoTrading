# AlgoTrading — Usage Guide (Offline / Online / Backtest / Paper / Kite)

This guide is written so you can **run each “type” of usage**, see what happens, and **correlate it with the exact script/module** that performs it.

> Scope note (important):
> - “Paper trading” here means *simulated orders/positions*.
> - The main menu’s “Live trading” option is marked *coming soon* in the code, so there is **no full continuous live trading loop** wired into the CLI yet.

---

## TL;DR Quick Start (pick one)

### A) Fastest: Launcher (offline/online chooser)

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\venv\Scripts\Activate.ps1
python start.py
```

### B) Offline (no internet; sample data)

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\venv\Scripts\Activate.ps1
python run_offline.py
```

### C) Online (internet; yfinance historical candles)

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\venv\Scripts\Activate.ps1
python run_online.py
```

### D) Run a backtest immediately (online)

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\venv\Scripts\Activate.ps1
python main.py
```

Then pick:
- `1` Backtest (single strategy)
- `2` Compare strategies
- `3` Paper trading session

### E) Kite (Zerodha) auth + verify (optional)

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\venv\Scripts\Activate.ps1
python authenticate.py
python test_kite_api.py
```

---

## 0) One-time setup (Windows PowerShell)

Run from the project folder:

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading

# Create venv
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env
copy .env.template .env
notepad .env
```

Correlate with code/docs:
- Setup guide: `SETUP.md`
- Dependencies: `requirements.txt`
- Config loader: `config/config.py`

---

## 1) Choose how you want to run it (recommended)

### Option A (recommended): Use the launcher menu

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\venv\Scripts\Activate.ps1
python start.py
```

What this runs:
- Launcher: `start.py`

### Option B: Run with the Windows launcher script

```powershell
cd C:\Users\lokeshwar.reddy\project\AlgoTrading
.\START.ps1
```

What this runs:
- PowerShell wrapper: `START.ps1` → calls `start.py`

---

## 2) OFFLINE MODE (no internet required)

Use this if you’re on a corporate network with SSL/proxy issues, or you just want repeatable test data.

### Run offline mode

```powershell
python run_offline.py
```

What you’ll see:
- A menu:
  - Backtest a Strategy
  - Compare Multiple Strategies
  - Test Risk Management
  - Generate Sample Data

What it actually does in code:
- Offline entrypoint: `run_offline.py`
  - Generates **sample OHLCV** locally (random volatility + trend-like behavior)
  - Uses strategies from `src/strategies/technical_strategies.py`
  - Uses backtester `src/backtesting/backtester.py`
  - Uses risk sizing from `src/risk_manager.py`
  - Uses simulated orders from `src/order_manager.py`

### Generate offline CSV data (optional)
In the offline menu choose “Generate Sample Data”. It saves to:
- `data/historical/<SYMBOL>_sample_<YYYYMMDD>.csv`

---

## 3) ONLINE MODE (internet required; still paper-trading by default)

Online mode primarily means: **real historical candles fetched from Yahoo Finance** (or NSEpy if configured).

### Run online mode

```powershell
python run_online.py
```

What this runs:
- `run_online.py` → calls `main.main()` in `main.py`

### Online mode main menu options
When `main.py` runs, it offers:
1. Backtest (single strategy)
2. Compare strategies
3. Paper trading session
4. Live trading (prints “coming soon”)

Correlate with code:
- CLI + orchestration: `main.py`
- Data fetcher: `src/data/data_handler.py`
- Strategies: `src/strategies/technical_strategies.py`
- Backtesting: `src/backtesting/backtester.py`
- Risk manager: `src/risk_manager.py`
- Paper order simulation: `src/order_manager.py`

---

## 4) Backtesting (the most “complete” workflow)

Backtesting is the most end-to-end path in this codebase.

### Backtest a single strategy

```powershell
python main.py
# Choose 1
# Enter symbol: RELIANCE
# Choose strategy: 1-5
```

What happens (in code order):
1. `config.validate()` ensures folders exist (`data/`, `data/historical/`, `logs/`).
2. `DataHandler.get_historical_data()` downloads daily candles.
3. Strategy calculates indicators and signals (`signal`: 1/0/-1).
4. `Backtester.run()` simulates trades across the series.
5. Summary prints to console.
6. Artifacts saved:
   - Plot: `logs/backtest_<SYMBOL>_<STRATEGY>_<YYYYMMDD>.png` (best-effort)
   - Trade log: `data/trades_<SYMBOL>_<STRATEGY>_<YYYYMMDD>.csv` (if trades exist)

Correlate with code:
- Backtest function: `run_backtest()` in `main.py`
- Simulator + metrics: `Backtester.run()` in `src/backtesting/backtester.py`

### Compare multiple strategies

```powershell
python main.py
# Choose 2
# Enter symbol: TCS
```

What happens:
- Calls `run_backtest()` repeatedly for each strategy and prints a comparison table.

---

## 5) Paper trading session (simulated orders; single-pass scan)

This is a *paper trading simulation* that places paper orders based on the **latest computed signal** per symbol.

### Run a paper trading session

```powershell
python main.py
# Choose 3
# Enter: RELIANCE,TCS,INFY
# Choose strategy: 1-5
```

Important behavior (so you correlate correctly):
- This is **not a continuous loop** that keeps running during the day.
- It fetches historical daily candles and looks at the **latest candle** to decide BUY/SELL.

What happens:
1. For each symbol, fetch data.
2. Compute `signal` for the latest row.
3. If BUY (`signal == 1`):
   - Computes stop-loss and take-profit
   - Computes position size
   - Places a paper BUY (opens a position)
4. If SELL (`signal == -1`) and a position exists in memory:
   - Places a paper SELL (closes position)
5. Saves positions snapshot:
   - `data/positions_<YYYYMMDD>.json`

Correlate with code:
- Paper trading loop: `paper_trading_session()` in `main.py`
- Risk sizing/limits: `src/risk_manager.py`
- Paper positions/orders: `src/order_manager.py`

---

## 6) Zerodha Kite (authentication + connection test)

Use this if you want to connect to Kite Connect (API key/secret + access token).

### Step 1 — Put Kite credentials in `.env`

Edit `.env`:

```ini
KITE_API_KEY=your_key
KITE_API_SECRET=your_secret
KITE_ACCESS_TOKEN=

TRADING_MODE=paper
DATA_SOURCE=yfinance
```

### Step 2 — Generate access token (daily)

```powershell
python authenticate.py
```

What it does:
- Opens the Kite login URL
- You paste `request_token`
- It writes `KITE_ACCESS_TOKEN` back into `.env`

Correlate with code:
- Auth script: `authenticate.py`

### Step 3 — Verify the token works

```powershell
python test_kite_api.py
```

What it does:
- Checks `KITE_API_KEY`, `KITE_API_SECRET`, and `KITE_ACCESS_TOKEN`
- Calls `kite.profile()` to confirm access

Correlate with code:
- Connection test: `test_kite_api.py`
- Broker wrapper: `src/broker.py`

### About “TRADING_MODE=live”
Setting `TRADING_MODE=live` enables real broker calls in `src/broker.py`.

However:
- `main.py` does **not** implement a complete live trading runtime loop yet.
- The “Live Trading” menu option currently prints that it’s coming soon.

---

## 7) Tests (quick ways to validate each type)

### Offline test (no internet)

```powershell
python test_offline.py
```

### Online test (requires internet)

```powershell
python test_online.py
```

### Full setup test (imports + data + strategy + backtest)

```powershell
python test_setup.py
```

---

## 8) Configuration recipes (copy/paste)

### A) Offline recipe (recommended on corporate network)

```ini
TRADING_MODE=paper
CAPITAL=100000
DATA_SOURCE=offline
KITE_API_KEY=
KITE_API_SECRET=
KITE_ACCESS_TOKEN=
```

Note: The offline menu uses internally generated data and does not rely on `DATA_SOURCE`, but keeping this set to `offline` documents your intent.

### B) Online recipe (paper trading using yfinance candles)

```ini
TRADING_MODE=paper
CAPITAL=100000
DATA_SOURCE=yfinance
```

### C) Online with Kite authentication (still mostly used for broker connection/tests)

```ini
TRADING_MODE=paper
DATA_SOURCE=yfinance
KITE_API_KEY=...
KITE_API_SECRET=...
KITE_ACCESS_TOKEN=...
```

---

## 9) Where outputs go (so you can verify)

- Logs:
  - `logs/trading_YYYYMMDD.log`
- Backtest plot (best-effort):
  - `logs/backtest_<SYMBOL>_<STRATEGY>_<YYYYMMDD>.png`
- Backtest trade log CSV:
  - `data/trades_<SYMBOL>_<STRATEGY>_<YYYYMMDD>.csv`
- Paper trading positions snapshot:
  - `data/positions_<YYYYMMDD>.json`
- Offline-generated sample OHLCV:
  - `data/historical/<SYMBOL>_sample_<YYYYMMDD>.csv`

---

## 10) Common troubleshooting (most frequent issues)

### “No data fetched” in online mode
- Check internet access.
- Try a well-known stock symbol (e.g., `RELIANCE`, `TCS`).
- Ensure `DATA_SOURCE=yfinance` (or try `nsepy`).

### Corporate SSL issues
- Use offline mode: `python run_offline.py`.
- Online code already disables SSL verification in `src/data/data_handler.py`, but corporate proxies can still block requests.

### Kite access token expired
- Run `python authenticate.py` again.
- Re-test with `python test_kite_api.py`.

---

## 11) “Correlation map” (feature → file)

- Offline menu: `run_offline.py`
- Online menu + orchestration: `main.py`
- Market data (yfinance/nsepy): `src/data/data_handler.py`
- Strategy logic + signals: `src/strategies/technical_strategies.py`
- Backtesting + metrics: `src/backtesting/backtester.py`
- Risk sizing + limits: `src/risk_manager.py`
- Paper orders/positions: `src/order_manager.py`
- Kite wrapper: `src/broker.py`
- Kite authentication: `authenticate.py`
- Kite connection test: `test_kite_api.py`
