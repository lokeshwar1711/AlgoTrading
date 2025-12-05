# Git Bash Quick Reference for AlgoTrading

## Setup (One-time)
```bash
# Activate virtual environment (if using bash)
source venv/Scripts/activate

# Or use Python directly from venv
alias python='venv/Scripts/python.exe'
```

## Quick Commands

### Authentication
```bash
# Get Kite API access token (required daily)
python authenticate.py
```

### Testing
```bash
# Test Kite API connection
python test_kite_api.py

# Test offline mode (no internet required)
python test_offline.py

# Test online mode (requires internet)
python test_online.py
```

### Running the System
```bash
# Quick launcher (choose offline/online)
python start.py

# Offline mode (no internet, uses sample data)
python run_offline.py

# Online mode (live data, requires authentication)
python run_online.py

# Full system with examples
python main.py
python examples.py
```

## SSH/Git Operations in Bash

### Check Git Status
```bash
git status
git log --oneline -5
```

### Push to GitHub
```bash
# Using Personal Access Token
git push https://YOUR_TOKEN@github.com/lokeshwar1711/AlgoTrading.git main

# Or configure once
git remote set-url origin https://YOUR_TOKEN@github.com/lokeshwar1711/AlgoTrading.git
git push
```

### Pull Latest Changes
```bash
git pull origin main
```

## Useful Bash Commands

### Navigate
```bash
pwd                     # Show current directory
ls -la                  # List all files
cd /c/Users/...         # Change directory (Git Bash uses /c/ for C:)
```

### Python Environment
```bash
# Check Python version
python --version

# Install packages
pip install package_name

# List installed packages
pip list

# Check if package is installed
pip show kiteconnect
```

### File Operations
```bash
# View file content
cat .env
head -20 src/broker.py

# Edit files
nano .env              # Simple text editor
vim .env               # If you know vim

# Search in files
grep -r "KITE_API" .
```

## UTF-8 Encoding for Bash

If you see encoding issues with ₹ symbol:
```bash
# Set UTF-8 encoding
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Add to ~/.bashrc for permanent fix
echo 'export PYTHONIOENCODING=utf-8' >> ~/.bashrc
```

## Quick Start Scripts

### For Bash Shell
```bash
# Make scripts executable (one time)
chmod +x *.sh

# Run any .sh script
bash start.sh
bash test_kite.sh

# Or directly (if executable)
./start.sh
./test_kite.sh
```

## Troubleshooting

### If Python not found
```bash
# Use full path
/c/Users/lokeshwar.reddy/project/venv/Scripts/python.exe test_kite_api.py
```

### If SSL errors (corporate network)
```bash
# Already handled in code, but if needed:
export PYTHONHTTPSVERIFY=0
python test_offline.py  # Use offline mode
```

### Check what's running
```bash
ps aux | grep python    # Show Python processes
netstat -an | grep 5000 # Check if port 5000 is in use
```

## Pro Tips

1. **Use Tab Completion**: Type part of filename and press Tab
2. **Command History**: Press ↑ to see previous commands
3. **Clear Screen**: Type `clear` or press Ctrl+L
4. **Stop Running Script**: Press Ctrl+C
5. **Background Process**: Add `&` at end: `python main.py &`

## Daily Workflow

```bash
# Morning setup (if access token expired)
python authenticate.py

# Verify connection
python test_kite_api.py

# Run trading system
python run_online.py

# Or use offline mode for strategy development
python run_offline.py
```

## Access Token Management

Access tokens expire daily at midnight. Before market open:
```bash
# Check if token works
python test_kite_api.py

# If expired, re-authenticate
python authenticate.py
```

---
**Note**: Git Bash uses Unix-style paths. Windows `C:\` becomes `/c/`
