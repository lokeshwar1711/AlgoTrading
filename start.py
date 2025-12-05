"""
TRADING SYSTEM LAUNCHER
Choose between OFFLINE or ONLINE mode
"""

import sys

print("\n" + "="*70)
print("ALGORITHMIC TRADING SYSTEM")
print("="*70 + "\n")

print("Choose your mode:\n")

print("1. OFFLINE MODE")
print("   - Works without internet")
print("   - Perfect for corporate networks")
print("   - Uses sample/cached data")
print("   - Test and develop strategies")
print()

print("2. ONLINE MODE") 
print("   - Requires internet connection")
print("   - Live market data from Yahoo Finance")
print("   - Zerodha API integration")
print("   - Backtesting with real data")
print()

print("3. Test Offline System")
print("   - Quick test without internet")
print()

print("4. Test Online System")
print("   - Test with live data (requires internet)")
print()

print("5. Authenticate Zerodha")
print("   - Setup Kite API access token")
print()

print("6. Exit")

choice = input("\nSelect option (1-6): ").strip()

if choice == '1':
    print("\nStarting OFFLINE mode...")
    import run_offline
elif choice == '2':
    print("\nStarting ONLINE mode...")
    print("Note: Requires internet connection\n")
    import run_online
elif choice == '3':
    print("\nRunning offline tests...\n")
    import subprocess
    subprocess.run([sys.executable, "test_offline.py"])
elif choice == '4':
    print("\nRunning online tests...\n")
    import subprocess
    subprocess.run([sys.executable, "test_online.py"])
elif choice == '5':
    print("\nStarting authentication...")
    import authenticate
elif choice == '6':
    print("\nExiting...")
else:
    print("\n⚠ Invalid choice!")
