"""
OFFLINE MODE - Run trading system without internet
Perfect for corporate networks with SSL/firewall restrictions
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("\n" + "="*70)
print("ALGORITHMIC TRADING SYSTEM - OFFLINE MODE")
print("="*70 + "\n")

print("Running in OFFLINE mode (no internet required)")
print("Using sample/cached data for testing\n")

def create_sample_data(symbol="SAMPLE", days=252):
    """Create realistic sample market data"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Create realistic price data with trend and volatility
    np.random.seed(42)
    returns = np.random.randn(days) * 0.02  # 2% daily volatility
    prices = 2500 * (1 + returns).cumprod()
    
    data = pd.DataFrame({
        'date': dates,
        'open': prices + np.random.randn(days) * 10,
        'high': prices + abs(np.random.randn(days)) * 15,
        'low': prices - abs(np.random.randn(days)) * 15,
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, days)
    })
    
    # Ensure high >= low, open, close
    data['high'] = data[['open', 'high', 'close']].max(axis=1)
    data['low'] = data[['open', 'low', 'close']].min(axis=1)
    
    return data

def menu():
    """Main menu for offline mode"""
    print("="*70)
    print("MAIN MENU")
    print("="*70)
    print("\n1. Backtest a Strategy")
    print("2. Compare Multiple Strategies")
    print("3. Test Risk Management")
    print("4. Generate Sample Data")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    return choice

def backtest_strategy():
    """Run backtest with sample data"""
    from src.strategies.technical_strategies import (
        MovingAverageCrossover, RSIStrategy, MACDStrategy, CombinedStrategy
    )
    from src.backtesting.backtester import Backtester
    
    print("\n" + "-"*70)
    print("BACKTEST STRATEGY")
    print("-"*70)
    
    print("\nAvailable Strategies:")
    print("1. Moving Average Crossover")
    print("2. RSI Strategy")
    print("3. MACD Strategy")
    print("4. Combined Strategy")
    
    choice = input("\nSelect strategy (1-4): ").strip()
    
    # Create sample data
    print("\nGenerating sample market data...")
    df = create_sample_data(symbol="SAMPLE_STOCK", days=252)
    print(f"✓ Created {len(df)} days of data")
    print(f"  Price range: ₹{df['close'].min():.2f} - ₹{df['close'].max():.2f}")
    
    # Select strategy
    if choice == '1':
        strategy = MovingAverageCrossover(short_window=20, long_window=50)
    elif choice == '2':
        strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    elif choice == '3':
        strategy = MACDStrategy(fast=12, slow=26, signal=9)
    else:
        strategy = CombinedStrategy()
    
    # Run backtest
    print(f"\nRunning backtest with {strategy.name}...")
    backtester = Backtester(strategy, initial_capital=100000)
    results = backtester.run(df, commission=0.001)
    
    # Show results
    backtester.print_summary()
    
    input("\nPress Enter to continue...")

def compare_strategies():
    """Compare multiple strategies"""
    from src.strategies.technical_strategies import (
        MovingAverageCrossover, RSIStrategy, MACDStrategy, CombinedStrategy
    )
    from src.backtesting.backtester import Backtester
    
    print("\n" + "-"*70)
    print("COMPARE STRATEGIES")
    print("-"*70)
    
    # Create sample data
    print("\nGenerating sample market data...")
    df = create_sample_data(symbol="SAMPLE_STOCK", days=365)
    print(f"✓ Created {len(df)} days of data")
    
    strategies = [
        ('MA Crossover', MovingAverageCrossover(20, 50)),
        ('RSI', RSIStrategy(14, 30, 70)),
        ('MACD', MACDStrategy(12, 26, 9)),
        ('Combined', CombinedStrategy())
    ]
    
    results_list = []
    
    print("\nTesting strategies...")
    for name, strategy in strategies:
        print(f"  Testing {name}...")
        backtester = Backtester(strategy, initial_capital=100000)
        result = backtester.run(df, commission=0.001)
        
        results_list.append({
            'Strategy': name,
            'Return (%)': f"{result['total_return']:.2f}",
            'Win Rate (%)': f"{result['win_rate']:.2f}",
            'Trades': result['total_trades'],
            'Sharpe': f"{result['sharpe_ratio']:.2f}",
            'Max DD (%)': f"{result['max_drawdown']:.2f}"
        })
    
    # Display comparison
    print("\n" + "="*80)
    print("STRATEGY COMPARISON RESULTS")
    print("="*80)
    
    results_df = pd.DataFrame(results_list)
    print(results_df.to_string(index=False))
    print("="*80 + "\n")
    
    input("Press Enter to continue...")

def test_risk_management():
    """Test risk management features"""
    from src.risk_manager import RiskManager
    from src.order_manager import OrderManager
    
    print("\n" + "-"*70)
    print("RISK MANAGEMENT TEST")
    print("-"*70)
    
    # Initialize risk manager
    capital = 100000
    risk_manager = RiskManager(capital=capital)
    
    print(f"\nInitial Capital: ₹{capital:,.2f}")
    print(f"Max Risk per Trade: {risk_manager.max_risk_per_trade}%")
    print(f"Max Daily Loss: {risk_manager.max_daily_loss}%")
    print(f"Max Open Positions: {risk_manager.max_open_positions}")
    
    # Example trade calculation
    entry_price = 2500
    stop_loss_pct = 2  # 2% stop loss
    stop_loss = risk_manager.calculate_stop_loss(entry_price, value=stop_loss_pct)
    
    quantity = risk_manager.calculate_position_size(entry_price, stop_loss)
    take_profit = risk_manager.calculate_take_profit(entry_price, stop_loss, reward_ratio=2)
    
    print(f"\nExample Trade Setup:")
    print(f"  Entry Price: ₹{entry_price:.2f}")
    print(f"  Stop Loss: ₹{stop_loss:.2f} ({stop_loss_pct}% risk)")
    print(f"  Take Profit: ₹{take_profit:.2f} (2:1 R:R)")
    print(f"  Position Size: {quantity} units")
    print(f"  Position Value: ₹{quantity * entry_price:,.2f}")
    print(f"  Risk Amount: ₹{quantity * (entry_price - stop_loss):,.2f}")
    
    # Test order manager
    order_manager = OrderManager(risk_manager=risk_manager)
    
    print(f"\nPlacing paper trade...")
    order_id = order_manager.place_order(
        symbol="SAMPLE",
        transaction_type="BUY",
        quantity=quantity,
        price=entry_price,
        stop_loss=stop_loss,
        take_profit=take_profit
    )
    
    if order_id:
        print(f"✓ Order placed: {order_id}")
        open_pos = order_manager.get_open_positions()
        print(f"  Open Positions: {len(open_pos)}")
    else:
        print("⚠ Order validation failed (position size too large)")
    
    # Risk metrics
    metrics = risk_manager.get_risk_metrics()
    print(f"\nCurrent Risk Metrics:")
    print(f"  Capital: ₹{metrics['capital']:,.2f}")
    print(f"  Daily P&L: ₹{metrics['daily_pnl']:,.2f}")
    print(f"  Open Positions: {metrics['open_positions']}/{metrics['max_open_positions']}")
    print(f"  Available Positions: {metrics['available_positions']}")
    
    input("\nPress Enter to continue...")

def generate_sample_data():
    """Generate and save sample data"""
    print("\n" + "-"*70)
    print("GENERATE SAMPLE DATA")
    print("-"*70)
    
    days = input("\nHow many days of data? (default 252): ").strip()
    days = int(days) if days else 252
    
    symbol = input("Stock symbol (default SAMPLE): ").strip().upper()
    symbol = symbol if symbol else "SAMPLE"
    
    print(f"\nGenerating {days} days of data for {symbol}...")
    df = create_sample_data(symbol=symbol, days=days)
    
    # Save to CSV
    filename = f"data/historical/{symbol}_sample_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✓ Data generated and saved to: {filename}")
    print(f"\nData Summary:")
    print(f"  Records: {len(df)}")
    print(f"  Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"  Price Range: ₹{df['close'].min():.2f} - ₹{df['close'].max():.2f}")
    print(f"  Average Volume: {df['volume'].mean():,.0f}")
    
    input("\nPress Enter to continue...")

def main():
    """Main application loop"""
    try:
        while True:
            choice = menu()
            
            if choice == '1':
                backtest_strategy()
            elif choice == '2':
                compare_strategies()
            elif choice == '3':
                test_risk_management()
            elif choice == '4':
                generate_sample_data()
            elif choice == '5':
                print("\nExiting...")
                break
            else:
                print("\n⚠ Invalid choice. Please select 1-5.")
                input("Press Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Note: This is OFFLINE mode - no real market data")
    print("Perfect for developing and testing strategies!\n")
    main()
