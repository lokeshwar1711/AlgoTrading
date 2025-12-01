"""
Simple tests to verify installation
Run with: python test_setup.py
"""

import sys


def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import pandas
        print("✓ pandas")
    except ImportError as e:
        print(f"✗ pandas: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import yfinance
        print("✓ yfinance")
    except ImportError as e:
        print(f"✗ yfinance: {e}")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib")
    except ImportError as e:
        print(f"✗ matplotlib: {e}")
        return False
    
    try:
        from kiteconnect import KiteConnect
        print("✓ kiteconnect")
    except ImportError as e:
        print(f"✗ kiteconnect: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv")
    except ImportError as e:
        print(f"✗ python-dotenv: {e}")
        return False
    
    print("\nAll required packages imported successfully!")
    return True


def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config.config import config
        print(f"✓ Config loaded")
        print(f"  - Trading Mode: {config.TRADING_MODE}")
        print(f"  - Capital: ₹{config.CAPITAL:,.2f}")
        print(f"  - Data Source: {config.DATA_SOURCE}")
        return True
    except Exception as e:
        print(f"✗ Config failed: {e}")
        return False


def test_data_fetch():
    """Test data fetching"""
    print("\nTesting data fetching...")
    
    try:
        from src.data.data_handler import DataHandler
        
        data_handler = DataHandler(data_source='yfinance')
        df = data_handler.get_historical_data('TCS', interval='1d')
        
        if not df.empty:
            print(f"✓ Data fetched successfully")
            print(f"  - Records: {len(df)}")
            print(f"  - Latest price: ₹{df['close'].iloc[-1]:.2f}")
            return True
        else:
            print("✗ No data fetched")
            return False
            
    except Exception as e:
        print(f"✗ Data fetch failed: {e}")
        return False


def test_strategy():
    """Test strategy creation"""
    print("\nTesting strategy...")
    
    try:
        from src.strategies.technical_strategies import MovingAverageCrossover
        from src.data.data_handler import DataHandler
        
        # Fetch data
        data_handler = DataHandler(data_source='yfinance')
        df = data_handler.get_historical_data('RELIANCE', interval='1d')
        
        # Create strategy
        strategy = MovingAverageCrossover(short_window=20, long_window=50)
        
        # Calculate indicators
        df = strategy.calculate_indicators(df)
        
        # Generate signals
        df = strategy.generate_signals(df)
        
        if 'signal' in df.columns:
            print("✓ Strategy working")
            latest_signal = df['signal'].iloc[-1]
            signal_text = {1: 'BUY', -1: 'SELL', 0: 'HOLD'}
            print(f"  - Latest signal: {signal_text[latest_signal]}")
            return True
        else:
            print("✗ Signal generation failed")
            return False
            
    except Exception as e:
        print(f"✗ Strategy test failed: {e}")
        return False


def test_backtester():
    """Test backtesting"""
    print("\nTesting backtester...")
    
    try:
        from src.backtesting.backtester import Backtester
        from src.strategies.technical_strategies import RSIStrategy
        from src.data.data_handler import DataHandler
        
        # Fetch data
        data_handler = DataHandler(data_source='yfinance')
        df = data_handler.get_historical_data('INFY', interval='1d')
        
        # Create strategy and backtest
        strategy = RSIStrategy(period=14)
        backtester = Backtester(strategy, initial_capital=100000)
        results = backtester.run(df, commission=0.001)
        
        if results:
            print("✓ Backtester working")
            print(f"  - Total Return: {results['total_return']:.2f}%")
            print(f"  - Total Trades: {results['total_trades']}")
            return True
        else:
            print("✗ Backtest failed")
            return False
            
    except Exception as e:
        print(f"✗ Backtester test failed: {e}")
        return False


def test_risk_manager():
    """Test risk manager"""
    print("\nTesting risk manager...")
    
    try:
        from src.risk_manager import RiskManager
        
        risk_manager = RiskManager(capital=100000)
        
        # Test position sizing
        entry_price = 2500
        stop_loss = 2450
        quantity = risk_manager.calculate_position_size(entry_price, stop_loss)
        
        if quantity > 0:
            print("✓ Risk manager working")
            print(f"  - Position size: {quantity} units")
            return True
        else:
            print("✗ Position sizing failed")
            return False
            
    except Exception as e:
        print(f"✗ Risk manager test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("TESTING TRADING SYSTEM INSTALLATION")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_config,
        test_data_fetch,
        test_strategy,
        test_backtester,
        test_risk_manager
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python examples.py' to see examples")
        print("2. Run 'python main.py' to start trading")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("1. Make sure virtual environment is activated")
        print("2. Run 'pip install -r requirements.txt'")
        print("3. Check your .env file configuration")
        print("4. Ensure you have internet connection")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
