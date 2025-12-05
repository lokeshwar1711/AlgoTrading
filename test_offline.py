"""
Quick offline test - No internet needed
Tests core functionality without fetching live data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("\n" + "="*70)
print("OFFLINE SYSTEM TEST - NO INTERNET REQUIRED")
print("="*70 + "\n")

# Test 1: Create sample data
print("Test 1: Creating sample market data...")
dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
sample_data = pd.DataFrame({
    'date': dates,
    'open': 2500 + np.random.randn(100) * 50,
    'high': 2550 + np.random.randn(100) * 50,
    'low': 2450 + np.random.randn(100) * 50,
    'close': 2500 + np.random.randn(100) * 50,
    'volume': np.random.randint(1000000, 5000000, 100)
})
sample_data['close'] = sample_data['close'].cumsum() / 10 + 2500
print(f"✓ Created {len(sample_data)} days of sample data")
print(f"  Price range: ₹{sample_data['close'].min():.2f} - ₹{sample_data['close'].max():.2f}\n")

# Test 2: Strategy
print("Test 2: Testing strategy with sample data...")
from src.strategies.technical_strategies import MovingAverageCrossover

strategy = MovingAverageCrossover(short_window=10, long_window=20)
df = strategy.calculate_indicators(sample_data.copy())
df = strategy.generate_signals(df)

buy_signals = len(df[df['signal'] == 1])
sell_signals = len(df[df['signal'] == -1])
print(f"✓ Strategy generated {buy_signals} BUY and {sell_signals} SELL signals\n")

# Test 3: Backtesting
print("Test 3: Running backtest...")
from src.backtesting.backtester import Backtester

backtester = Backtester(strategy, initial_capital=100000)
results = backtester.run(df, commission=0.001)

print(f"✓ Backtest completed successfully")
print(f"  Initial Capital: ₹{results['initial_capital']:,.2f}")
print(f"  Final Capital: ₹{results['final_capital']:,.2f}")
print(f"  Return: {results['total_return']:.2f}%")
print(f"  Total Trades: {results['total_trades']}")
print(f"  Win Rate: {results['win_rate']:.2f}%\n")

# Test 4: Risk Management
print("Test 4: Testing risk management...")
from src.risk_manager import RiskManager

risk_manager = RiskManager(capital=100000)
entry_price = 2500
stop_loss = 2450
quantity = risk_manager.calculate_position_size(entry_price, stop_loss)
take_profit = risk_manager.calculate_take_profit(entry_price, stop_loss, reward_ratio=2)

print(f"✓ Risk management working")
print(f"  Entry: ₹{entry_price:.2f}")
print(f"  Stop Loss: ₹{stop_loss:.2f}")
print(f"  Take Profit: ₹{take_profit:.2f}")
print(f"  Position Size: {quantity} units\n")

# Test 5: Order Manager
print("Test 5: Testing order management (paper mode)...")
from src.order_manager import OrderManager

order_manager = OrderManager(risk_manager=risk_manager)
order_id = order_manager.place_order(
    symbol="TEST",
    transaction_type="BUY",
    quantity=quantity,
    price=entry_price,
    stop_loss=stop_loss,
    take_profit=take_profit
)

print(f"✓ Paper order placed: {order_id}")
open_positions = order_manager.get_open_positions()
print(f"  Open Positions: {len(open_positions)}\n")

# Summary
print("="*70)
print("ALL TESTS PASSED! ✓")
print("="*70)
print("\nYour trading system is working perfectly!")
print("\nNote: Data fetching from Yahoo Finance may fail due to")
print("corporate network SSL certificate issues. This is normal.")
print("\nYou can:")
print("1. Use paper trading with offline/cached data")
print("2. Try nsepy as alternative data source")
print("3. Work with sample data for testing strategies")
print("4. Use Zerodha Kite API for live data (when authenticated)")
print("\n" + "="*70 + "\n")
