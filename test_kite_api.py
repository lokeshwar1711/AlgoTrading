#!/usr/bin/env python3
"""
Test Kite API Connection
Tests if the API credentials are valid and can connect to Zerodha
"""

import os
import sys
from pathlib import Path

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠ python-dotenv not installed, using system environment variables")

# Simple colored print functions
def print_info(msg):
    print(f"ℹ {msg}")

def print_success(msg):
    print(f"✓ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_warning(msg):
    print(f"⚠ {msg}")

def print_header(msg):
    print(f"\n{'=' * 70}")
    print(msg)
    print(f"{'=' * 70}")

def test_kite_credentials():
    """Test if Kite API credentials are configured"""
    print_header("ZERODHA KITE API CONNECTION TEST")
    
    api_key = os.getenv("KITE_API_KEY")
    api_secret = os.getenv("KITE_API_SECRET")
    
    if not api_key or api_key == "your_api_key_here":
        print_error("KITE_API_KEY not configured in .env file")
        print_info("\nPlease update your .env file with:")
        print_info("  KITE_API_KEY=your_actual_api_key")
        return False
    
    if not api_secret or api_secret == "your_api_secret_here":
        print_error("KITE_API_SECRET not configured in .env file")
        print_info("\nPlease update your .env file with:")
        print_info("  KITE_API_SECRET=your_actual_api_secret")
        return False
    
    print_success(f"KITE_API_KEY found: {api_key[:8]}...")
    print_success(f"KITE_API_SECRET found: {api_secret[:8]}...")
    
    return True

def test_kite_connection():
    """Test actual connection to Kite API"""
    try:
        from kiteconnect import KiteConnect
        
        api_key = os.getenv("KITE_API_KEY")
        kite = KiteConnect(api_key=api_key)
        
        print_header("Testing Kite API Connection...")
        
        # Get login URL
        login_url = kite.login_url()
        print_success("Successfully created Kite instance")
        print_success("API Key is valid format")
        
        # Check if we have an access token
        access_token = os.getenv("KITE_ACCESS_TOKEN")
        
        if not access_token or access_token.strip() == "":
            print_warning("No access token found")
            print_info("\nTo get an access token:")
            print_info("1. Run: python authenticate.py")
            print_info("2. Or manually visit this URL:")
            print_info(f"   {login_url}")
            print_info("3. After login, you'll get a request token")
            print_info("4. Use that to generate access token")
            return False
        
        # Try to set access token and make a test call
        kite.set_access_token(access_token)
        print_success(f"Access token found: {access_token[:8]}...")
        
        try:
            # Test API call - get profile
            print_info("\nTesting API call: Getting user profile...")
            profile = kite.profile()
            
            print_header("✅ CONNECTION SUCCESSFUL!")
            print_info("\nUser Details:")
            print_info(f"  User ID: {profile.get('user_id', 'N/A')}")
            print_info(f"  Name: {profile.get('user_name', 'N/A')}")
            print_info(f"  Email: {profile.get('email', 'N/A')}")
            print_info(f"  Broker: {profile.get('broker', 'N/A')}")
            
            # Test getting instruments
            print_info(f"\nTesting instrument data...")
            try:
                instruments = kite.instruments("NSE")
                print_success(f"Successfully fetched {len(instruments)} instruments from NSE")
            except Exception as e:
                print_warning(f"Could not fetch instruments: {e}")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            print_error(f"API Call Failed: {error_msg}")
            
            if "Invalid access token" in error_msg or "TokenException" in error_msg:
                print_info("\nYour access token is invalid or expired.")
                print_info("Access tokens expire daily. Please refresh by running:")
                print_info("  python authenticate.py")
            elif "403" in error_msg:
                print_info("\nAPI access forbidden. Please check:")
                print_info("  1. Your API key is active on Kite Connect")
                print_info("  2. Your app is enabled")
                print_info("  3. You have required permissions")
            else:
                print_info("\nPlease check your credentials and try again")
            
            return False
            
    except ImportError:
        print_error("kiteconnect library not installed")
        print_info("Run: pip install kiteconnect")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """Main test function"""
    print_info("\n🔍 Starting Kite API connection test...\n")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print_error(".env file not found!")
        print_info("\nPlease create .env file from template:")
        print_info("  1. Copy .env.template to .env")
        print_info("  2. Add your Kite API credentials")
        print_info("  3. Run this test again")
        return
    
    # Test credentials
    if not test_kite_credentials():
        return
    
    # Test connection
    success = test_kite_connection()
    
    # Summary
    print_header("")
    if success:
        print_success("ALL TESTS PASSED!")
        print_info("Your Kite API is properly configured and connected.")
        print_info("\nYou can now run:")
        print_info("  python run_online.py    (for live trading)")
        print_info("  python main.py          (full system)")
    else:
        print_warning("TESTS INCOMPLETE")
        print_info("Please follow the instructions above to complete setup.")
    print("=" * 70)

if __name__ == "__main__":
    main()
