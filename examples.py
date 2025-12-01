"""
Quick Start Examples
Demonstrates how to use the trading system
"""

from config.config import config
from src.data.data_handler import DataHandler
from src.strategies.technical_strategies import (
    MovingAverageCrossover, RSIStrategy, CombinedStrategy
)
from src.backtesting.backtester import Backtester


def example_1_fetch_data():
    """Example 1: Fetch historical data"""
    print("\n=== Example 1: Fetch Historical Data ===\n")
    
    data_handler = DataHandler(data_source='yfinance')
    
    # Fetch data for a single stock
    df = data_handler.get_historical_data('RELIANCE')
    print(f"Fetched {len(df)} records for RELIANCE")
    print(df.head())
    
    # Fetch data for multiple stocks
    symbols = ['TCS', 'INFY', 'WIPRO']
    data = data_handler.get_multiple_stocks(symbols)
    print(f"\nFetched data for {len(data)} stocks")
    

def example_2_simple_strategy():
    """Example 2: Create and test a simple strategy"""
    print("\n=== Example 2: Simple MA Crossover Strategy ===\n")
    
    # Fetch data
    data_handler = DataHandler(data_source='yfinance')
    df = data_handler.get_historical_data('TCS')
    
    # Create strategy
    strategy = MovingAverageCrossover(short_window=20, long_window=50)
    
    # Calculate indicators
    df = strategy.calculate_indicators(df)
    print("Indicators calculated:")
    print(df[['date', 'close', 'ma_short', 'ma_long']].tail())
    
    # Generate signals
    df = strategy.generate_signals(df)
    
    # Show latest signal
    latest_signal = df['signal'].iloc[-1]
    signal_text = {1: 'BUY', -1: 'SELL', 0: 'HOLD'}
    print(f"\nLatest signal for TCS: {signal_text[latest_signal]}")


def example_3_backtest():
    """Example 3: Run a backtest"""
    print("\n=== Example 3: Backtest a Strategy ===\n")
    
    # Fetch data
    data_handler = DataHandler(data_source='yfinance')
    df = data_handler.get_historical_data('HDFCBANK')
    
    # Create strategy
    strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    
    # Run backtest
    backtester = Backtester(strategy, initial_capital=100000)
    results = backtester.run(df, commission=0.001)
    
    # Print summary
    backtester.print_summary()
    
    # Get trade log
    trade_log = backtester.get_trade_log()
    print("\nFirst 5 trades:")
    print(trade_log.head())


def example_4_compare_strategies():
    """Example 4: Compare multiple strategies"""
    print("\n=== Example 4: Compare Strategies ===\n")
    
    # Fetch data
    data_handler = DataHandler(data_source='yfinance')
    df = data_handler.get_historical_data('INFY')
    
    strategies = [
        ('MA Crossover', MovingAverageCrossover(20, 50)),
        ('RSI', RSIStrategy(14, 30, 70)),
        ('Combined', CombinedStrategy())
    ]
    
    results = []
    
    for name, strategy in strategies:
        backtester = Backtester(strategy, initial_capital=100000)
        result = backtester.run(df, commission=0.001)
        
        results.append({
            'Strategy': name,
            'Return (%)': f"{result['total_return']:.2f}",
            'Win Rate (%)': f"{result['win_rate']:.2f}",
            'Sharpe Ratio': f"{result['sharpe_ratio']:.2f}",
            'Max DD (%)': f"{result['max_drawdown']:.2f}"
        })
    
    print("\nStrategy Comparison for INFY:")
    print("-" * 70)
    for r in results:
        print(f"{r['Strategy']:15} | Return: {r['Return (%)']}% | "
              f"Win Rate: {r['Win Rate (%)']}% | Sharpe: {r['Sharpe Ratio']}")


def example_5_risk_management():
    """Example 5: Risk management calculations"""
    print("\n=== Example 5: Risk Management ===\n")
    
    from src.risk_manager import RiskManager
    
    risk_manager = RiskManager(capital=100000)
    
    # Calculate position size
    entry_price = 2500
    stop_loss = 2450  # 2% stop loss
    
    quantity = risk_manager.calculate_position_size(entry_price, stop_loss)
    print(f"Entry Price: ₹{entry_price}")
    print(f"Stop Loss: ₹{stop_loss}")
    print(f"Recommended Quantity: {quantity}")
    
    # Calculate take profit
    take_profit = risk_manager.calculate_take_profit(entry_price, stop_loss, reward_ratio=2)
    print(f"Take Profit (2:1 R:R): ₹{take_profit:.2f}")
    
    # Get risk metrics
    metrics = risk_manager.get_risk_metrics()
    print("\nRisk Metrics:")
    print(f"  Capital: ₹{metrics['capital']:,.2f}")
    print(f"  Max Risk per Trade: {metrics['max_risk_per_trade']}%")
    print(f"  Max Open Positions: {metrics['max_open_positions']}")


def example_6_nifty50_scan():
    """Example 6: Scan Nifty 50 stocks for signals"""
    print("\n=== Example 6: Scan Nifty 50 for Signals ===\n")
    
    data_handler = DataHandler(data_source='yfinance')
    strategy = CombinedStrategy()
    
    # Get Nifty 50 stocks
    nifty50 = data_handler.get_nifty_50_stocks()[:10]  # First 10 for demo
    
    signals = []
    
    print("Scanning stocks...")
    for symbol in nifty50:
        try:
            df = data_handler.get_historical_data(symbol)
            if not df.empty:
                signal = strategy.get_current_signal(df)
                current_price = df['close'].iloc[-1]
                
                if signal != 0:  # Only show buy/sell signals
                    signal_text = 'BUY' if signal == 1 else 'SELL'
                    signals.append({
                        'Symbol': symbol,
                        'Signal': signal_text,
                        'Price': f"₹{current_price:.2f}"
                    })
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
    
    if signals:
        print("\nStocks with active signals:")
        print("-" * 40)
        for s in signals:
            print(f"{s['Symbol']:12} | {s['Signal']:4} | {s['Price']}")
    else:
        print("\nNo active signals found")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("ALGORITHMIC TRADING SYSTEM - EXAMPLES")
    print("="*70)
    
    # Validate configuration
    config.validate()
    
    print("\nSelect an example to run:")
    print("1. Fetch Historical Data")
    print("2. Simple Strategy")
    print("3. Backtest a Strategy")
    print("4. Compare Strategies")
    print("5. Risk Management")
    print("6. Scan Nifty 50 for Signals")
    print("7. Run All Examples")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-7): ").strip()
    
    examples = {
        '1': example_1_fetch_data,
        '2': example_2_simple_strategy,
        '3': example_3_backtest,
        '4': example_4_compare_strategies,
        '5': example_5_risk_management,
        '6': example_6_nifty50_scan,
    }
    
    if choice == '7':
        for func in examples.values():
            try:
                func()
                print("\n" + "-"*70)
            except Exception as e:
                print(f"Error: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"Error: {e}")
    elif choice == '0':
        print("Exiting...")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
