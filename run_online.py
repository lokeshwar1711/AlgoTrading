"""
ONLINE MODE - Full trading system with live data
Requires internet connection and optionally Zerodha API
"""

import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import main application
from main import main

if __name__ == "__main__":
    print("\n" + "="*70)
    print("ALGORITHMIC TRADING SYSTEM - ONLINE MODE")
    print("="*70)
    print("\nRunning with live market data from Yahoo Finance")
    print("Zerodha API integration available for live trading\n")
    
    print("Requirements:")
    print("  ✓ Internet connection")
    print("  ✓ yfinance data access")
    print("  ⏸ Zerodha API (optional - for live trading)\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nIf you're on a corporate network with SSL issues,")
        print("try running in OFFLINE mode instead:")
        print("  python run_offline.py")
