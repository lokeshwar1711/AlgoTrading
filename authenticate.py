#!/usr/bin/env python3
"""
Zerodha Kite API Authentication
This script helps you generate an access token for Kite API
"""

import os
import webbrowser
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()

def print_header(msg):
    print(f"\n{'=' * 70}")
    print(msg)
    print(f"{'=' * 70}")

def print_info(msg):
    print(f"ℹ {msg}")

def print_success(msg):
    print(f"✓ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def authenticate():
    """
    Authenticate with Zerodha Kite API
    """
    try:
        from kiteconnect import KiteConnect
    except ImportError:
        print_error("kiteconnect library not installed")
        print_info("Run: pip install kiteconnect")
        return

    print_header("ZERODHA KITE API AUTHENTICATION")
    
    # Get API credentials
    api_key = os.getenv("KITE_API_KEY")
    api_secret = os.getenv("KITE_API_SECRET")
    
    if not api_key or api_key == "your_api_key_here":
        print_error("KITE_API_KEY not configured in .env file")
        print_info("Please update your .env file with your API key")
        return
    
    if not api_secret or api_secret == "your_api_secret_here":
        print_error("KITE_API_SECRET not configured in .env file")
        print_info("Please update your .env file with your API secret")
        return
    
    print_success(f"API Key: {api_key[:8]}...")
    print_success(f"API Secret: {api_secret[:8]}...")
    
    # Initialize Kite Connect
    kite = KiteConnect(api_key=api_key)
    
    # Get login URL
    login_url = kite.login_url()
    
    print("\n" + "=" * 70)
    print_info("Step 1: Login to Kite")
    print("=" * 70)
    print(f"\nOpening browser to: {login_url}")
    print_info("If browser doesn't open automatically, copy this URL:")
    print(f"  {login_url}\n")
    
    # Try to open browser
    try:
        webbrowser.open(login_url)
        print_success("Browser opened successfully")
    except:
        print_error("Could not open browser automatically")
        print_info("Please copy the URL above and open it manually")
    
    print("\n" + "=" * 70)
    print_info("Step 2: Get Request Token")
    print("=" * 70)
    print("""
After logging in:
1. You'll be redirected to a URL like:
   http://127.0.0.1:5000/?request_token=XXXXXX&action=login&status=success
   
2. Copy the 'request_token' value from the URL
   (It's the long string after request_token=)
    """)
    
    # Get request token from user
    request_token = input("\nPaste your request_token here: ").strip()
    
    if not request_token:
        print_error("No request token provided")
        return
    
    print("\n" + "=" * 70)
    print_info("Step 3: Generate Access Token")
    print("=" * 70)
    
    try:
        # Generate session
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        
        print_success("Access token generated successfully!")
        print(f"\nAccess Token: {access_token[:20]}...")
        
        # Save to .env file
        env_file = ".env"
        set_key(env_file, "KITE_ACCESS_TOKEN", access_token)
        
        print_success(f"Access token saved to {env_file}")
        
        # Verify by getting profile
        kite.set_access_token(access_token)
        profile = kite.profile()
        
        print("\n" + "=" * 70)
        print_success("✅ AUTHENTICATION SUCCESSFUL!")
        print("=" * 70)
        print(f"\nUser Details:")
        print(f"  User ID: {profile.get('user_id', 'N/A')}")
        print(f"  Name: {profile.get('user_name', 'N/A')}")
        print(f"  Email: {profile.get('email', 'N/A')}")
        print(f"  Broker: {profile.get('broker', 'N/A')}")
        
        print("\n" + "=" * 70)
        print_info("Next Steps:")
        print("=" * 70)
        print("""
✓ Your access token is now saved in .env file
✓ You can now run the trading system with live data

Try these commands:
  python test_kite_api.py     (verify connection)
  python run_online.py        (online trading mode)
  python main.py              (full trading system)

Note: Access tokens expire daily. Run this script again tomorrow.
        """)
        
    except Exception as e:
        print_error(f"Authentication failed: {e}")
        print_info("\nPossible issues:")
        print_info("  1. Invalid request token (they expire quickly)")
        print_info("  2. Request token already used (get a new one)")
        print_info("  3. Wrong API secret")
        print_info("  4. Network connectivity issues")
        print_info("\nTry running this script again with a fresh request token")

if __name__ == "__main__":
    authenticate()
