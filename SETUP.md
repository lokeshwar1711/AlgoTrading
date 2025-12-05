# Quick Setup Guide

## 🎯 Two Modes Available

- **OFFLINE MODE**: Test and develop strategies without internet (recommended for corporate networks)
- **ONLINE MODE**: Full functionality with live data (requires internet access)

---

## 📦 Step 1: Create Virtual Environment

```powershell
# Navigate to project directory
cd C:\Users\lokeshwar.reddy\project\AlgoTrading

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# OR for Command Prompt
venv\Scripts\activate.bat
```

---

## 📥 Step 2: Install Dependencies

```powershell
# Make sure venv is activated (you should see (venv) in prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: Installation takes 2-3 minutes. If any package fails, that's okay - core packages will work.

---

## ⚙️ Step 3: Configure Environment

```powershell
# Copy the template (if not done already)
copy .env.template .env

# Edit .env file
notepad .env
```

**For OFFLINE MODE** (Corporate Network):
```ini
TRADING_MODE=paper
CAPITAL=100000
DATA_SOURCE=offline
KITE_API_KEY=
KITE_API_SECRET=
KITE_ACCESS_TOKEN=
```

**For ONLINE MODE** (With Internet):
```ini
TRADING_MODE=paper
CAPITAL=100000
DATA_SOURCE=yfinance
KITE_API_KEY=your_key_here
KITE_API_SECRET=your_secret_here
KITE_ACCESS_TOKEN=
```

---

## ✅ Step 4: Test Installation

### OFFLINE Test (No Internet Needed):
```powershell
python test_offline.py
```

### ONLINE Test (Requires Internet):
```powershell
python test_online.py
```

---

## 🚀 Step 5: Start Trading

Choose based on your mode:

### OFFLINE Mode Scripts:
```powershell
# Test strategies with sample data
python run_offline.py

# Run backtests with sample data
python examples_offline.py
```

### ONLINE Mode Scripts:
```powershell
# Full system with live data
python main.py

# Examples with real market data
python examples.py

# Authenticate with Zerodha
python authenticate.py
```

---

## 🌐 ONLINE MODE Setup (For Home/Personal Machine)

If you want to use the system with live market data:

### 1. Setup Zerodha Kite API

```powershell
# Create Kite Connect App at: https://developers.kite.trade/apps/new
# Use these settings:
#   Redirect URL: http://127.0.0.1:5000
#   Postback URL: (leave blank)
```

### 2. Update .env with API Credentials

```ini
KITE_API_KEY=your_actual_api_key
KITE_API_SECRET=your_actual_api_secret
TRADING_MODE=paper
DATA_SOURCE=yfinance
```

### 3. Authenticate

```powershell
python authenticate.py
```

Follow the prompts to get your access token.

### 4. Run Online System

```powershell
python main.py
```

---

## 🔧 Troubleshooting

### Issue: SSL Certificate Error (Corporate Network)
**Solution**: Use OFFLINE mode
```powershell
python run_offline.py
```

### Issue: "Module not found"
**Solution**: Activate venv and reinstall
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Unicode (₹) not displaying
**Solution**: Run with UTF-8 encoding
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
python your_script.py
```

### Issue: Virtual environment activation fails
**Solution**: Enable script execution
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 Quick Command Reference

| Task | Offline | Online |
|------|---------|--------|
| **Test System** | `python test_offline.py` | `python test_online.py` |
| **Run Examples** | `python examples_offline.py` | `python examples.py` |
| **Start Trading** | `python run_offline.py` | `python main.py` |
| **Backtest** | `python run_offline.py` → Option 1 | `python main.py` → Option 1 |
| **Paper Trade** | `python run_offline.py` → Option 2 | `python main.py` → Option 3 |

---

## 💡 Recommended Workflow

**On Corporate Network (Offline)**:
1. Develop and test strategies offline
2. Use sample/historical data
3. Perfect your strategy logic
4. Export strategy code

**On Personal Network (Online)**:
1. Import your strategy
2. Backtest with real data
3. Paper trade with live data
4. Move to live trading (when ready)

---

## 🎓 Next Steps

1. ✅ Complete setup above
2. ✅ Run offline test: `python test_offline.py`
3. ✅ Try examples: `python run_offline.py`
4. ✅ Create your first strategy
5. ✅ Backtest thoroughly
6. ⏸️ Setup online mode (when ready)
7. ⏸️ Paper trade
8. ⏸️ Live trade (with caution)

---

## 📞 Support

- Check logs in `logs/` directory
- Review configuration in `.env`
- See full documentation in `README.md`
- Kite API docs: https://kite.trade/docs/connect/v3/

---

**Ready to start? Run `python test_offline.py` or `python test_online.py`!** 🚀
