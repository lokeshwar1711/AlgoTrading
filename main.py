"""
Main Trading Application
Orchestrates the entire trading system
"""

import sys
from datetime import datetime
from config.config import config
from src.broker import ZerodhaBroker
from src.data.data_handler import DataHandler
from src.strategies.technical_strategies import (
    MovingAverageCrossover, RSIStrategy, MACDStrategy, 
    BollingerBandsStrategy, CombinedStrategy
)
from src.backtesting.backtester import Backtester
from src.risk_manager import RiskManager
from src.order_manager import OrderManager
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_backtest(symbol, strategy_name='MA_Crossover', days=365):
    """
    Run backtest for a strategy
    
    Args:
        symbol: Stock symbol to backtest
        strategy_name: Name of strategy to use
        days: Number of days of historical data
    """
    logger.info(f"Starting backtest for {symbol} with {strategy_name}")
    
    # Fetch data
    data_handler = DataHandler(data_source=config.DATA_SOURCE)
    df = data_handler.get_historical_data(symbol, interval='1d')
    
    if df.empty:
        logger.error(f"No data available for {symbol}")
        return
    
    logger.info(f"Loaded {len(df)} data points for {symbol}")
    
    # Select strategy
    if strategy_name == 'MA_Crossover':
        strategy = MovingAverageCrossover(short_window=20, long_window=50, ma_type='SMA')
    elif strategy_name == 'RSI':
        strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    elif strategy_name == 'MACD':
        strategy = MACDStrategy(fast=12, slow=26, signal=9)
    elif strategy_name == 'BB':
        strategy = BollingerBandsStrategy(period=20, std_dev=2)
    elif strategy_name == 'Combined':
        strategy = CombinedStrategy()
    else:
        logger.error(f"Unknown strategy: {strategy_name}")
        return
    
    # Run backtest
    backtester = Backtester(strategy, initial_capital=config.CAPITAL)
    results = backtester.run(df, commission=0.001)
    
    # Print results
    backtester.print_summary()
    
    # Plot results
    try:
        plot_path = config.LOGS_DIR / f"backtest_{symbol}_{strategy_name}_{datetime.now().strftime('%Y%m%d')}.png"
        backtester.plot_results(df, save_path=plot_path)
    except Exception as e:
        logger.warning(f"Could not generate plot: {e}")
    
    # Save trade log
    trade_log = backtester.get_trade_log()
    if not trade_log.empty:
        log_path = config.DATA_DIR / f"trades_{symbol}_{strategy_name}_{datetime.now().strftime('%Y%m%d')}.csv"
        trade_log.to_csv(log_path, index=False)
        logger.info(f"Trade log saved to {log_path}")
    
    return results


def compare_strategies(symbol, strategies=None):
    """
    Compare multiple strategies on the same stock
    
    Args:
        symbol: Stock symbol
        strategies: List of strategy names
    """
    if strategies is None:
        strategies = ['MA_Crossover', 'RSI', 'MACD', 'BB', 'Combined']
    
    logger.info(f"Comparing strategies for {symbol}")
    
    results_summary = []
    
    for strategy_name in strategies:
        try:
            results = run_backtest(symbol, strategy_name)
            if results:
                results_summary.append({
                    'Strategy': strategy_name,
                    'Return (%)': results['total_return'],
                    'Win Rate (%)': results['win_rate'],
                    'Trades': results['total_trades'],
                    'Sharpe Ratio': results['sharpe_ratio'],
                    'Max DD (%)': results['max_drawdown']
                })
        except Exception as e:
            logger.error(f"Failed to backtest {strategy_name}: {e}")
    
    # Print comparison
    if results_summary:
        import pandas as pd
        df_summary = pd.DataFrame(results_summary)
        print("\n" + "="*80)
        print(f"STRATEGY COMPARISON FOR {symbol}")
        print("="*80)
        print(df_summary.to_string(index=False))
        print("="*80 + "\n")


def paper_trading_session(symbols, strategy_name='Combined'):
    """
    Run a paper trading session
    
    Args:
        symbols: List of symbols to trade
        strategy_name: Strategy to use
    """
    logger.info(f"Starting paper trading session with {strategy_name}")
    
    # Initialize components
    broker = ZerodhaBroker() if config.TRADING_MODE == 'live' else None
    risk_manager = RiskManager(capital=config.CAPITAL)
    order_manager = OrderManager(broker=broker, risk_manager=risk_manager)
    data_handler = DataHandler(data_source=config.DATA_SOURCE)
    
    # Select strategy
    if strategy_name == 'MA_Crossover':
        strategy = MovingAverageCrossover(short_window=20, long_window=50)
    elif strategy_name == 'RSI':
        strategy = RSIStrategy()
    elif strategy_name == 'MACD':
        strategy = MACDStrategy()
    elif strategy_name == 'BB':
        strategy = BollingerBandsStrategy()
    else:
        strategy = CombinedStrategy()
    
    # Trading loop
    for symbol in symbols:
        try:
            logger.info(f"Processing {symbol}")
            
            # Get data
            df = data_handler.get_historical_data(symbol, interval='1d')
            if df.empty:
                logger.warning(f"No data for {symbol}")
                continue
            
            # Get signal
            signal = strategy.get_current_signal(df)
            current_price = df['close'].iloc[-1]
            
            logger.info(f"{symbol}: Signal = {signal}, Price = ₹{current_price:.2f}")
            
            # Execute trades based on signal
            if signal == 1:  # Buy signal
                # Calculate position size
                stop_loss = risk_manager.calculate_stop_loss(current_price, value=2)
                quantity = risk_manager.calculate_position_size(current_price, stop_loss)
                
                if quantity > 0:
                    take_profit = risk_manager.calculate_take_profit(current_price, stop_loss)
                    
                    order_id = order_manager.place_order(
                        symbol=symbol,
                        transaction_type="BUY",
                        quantity=quantity,
                        price=current_price,
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )
                    
                    if order_id:
                        logger.info(f"BUY order placed: {symbol} x{quantity} @ ₹{current_price:.2f}")
            
            elif signal == -1 and symbol in order_manager.positions:  # Sell signal
                position = order_manager.positions[symbol]
                order_manager.place_order(
                    symbol=symbol,
                    transaction_type="SELL",
                    quantity=position.quantity,
                    price=current_price
                )
                logger.info(f"SELL order placed: {symbol} @ ₹{current_price:.2f}")
                
        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("PAPER TRADING SESSION SUMMARY")
    print("="*60)
    
    open_positions = order_manager.get_open_positions()
    print(f"Open Positions: {len(open_positions)}")
    for symbol, pos in open_positions.items():
        print(f"  {symbol}: {pos['quantity']:.2f} @ ₹{pos['entry_price']:.2f}")
    
    risk_metrics = risk_manager.get_risk_metrics()
    print(f"\nCapital: ₹{risk_metrics['capital']:,.2f}")
    print(f"Daily P&L: ₹{risk_metrics['daily_pnl']:,.2f} ({risk_metrics['daily_pnl_percentage']:.2f}%)")
    print(f"Open Positions: {risk_metrics['open_positions']}/{risk_metrics['max_open_positions']}")
    print("="*60 + "\n")
    
    # Save positions
    positions_file = config.DATA_DIR / f"positions_{datetime.now().strftime('%Y%m%d')}.json"
    order_manager.save_positions(positions_file)


def main():
    """Main entry point"""
    # Validate configuration
    config.validate()
    
    print("\n" + "="*60)
    print("ALGORITHMIC TRADING SYSTEM")
    print("="*60)
    print(f"Mode: {config.TRADING_MODE.upper()}")
    print(f"Capital: ₹{config.CAPITAL:,.2f}")
    print(f"Data Source: {config.DATA_SOURCE}")
    print("="*60 + "\n")
    
    # Menu
    print("Select an option:")
    print("1. Run Backtest (Single Strategy)")
    print("2. Compare Multiple Strategies")
    print("3. Paper Trading Session")
    print("4. Live Trading (requires Zerodha API)")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip().upper()
        print("\nAvailable strategies:")
        print("1. MA_Crossover")
        print("2. RSI")
        print("3. MACD")
        print("4. BB (Bollinger Bands)")
        print("5. Combined")
        
        strategy_choice = input("Select strategy (1-5): ").strip()
        strategy_map = {'1': 'MA_Crossover', '2': 'RSI', '3': 'MACD', '4': 'BB', '5': 'Combined'}
        strategy_name = strategy_map.get(strategy_choice, 'Combined')
        
        run_backtest(symbol, strategy_name)
    
    elif choice == '2':
        symbol = input("Enter stock symbol (e.g., RELIANCE): ").strip().upper()
        compare_strategies(symbol)
    
    elif choice == '3':
        symbols_input = input("Enter stock symbols (comma-separated, e.g., RELIANCE,TCS,INFY): ")
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        
        print("\nAvailable strategies:")
        print("1. MA_Crossover")
        print("2. RSI")
        print("3. MACD")
        print("4. BB (Bollinger Bands)")
        print("5. Combined")
        
        strategy_choice = input("Select strategy (1-5): ").strip()
        strategy_map = {'1': 'MA_Crossover', '2': 'RSI', '3': 'MACD', '4': 'BB', '5': 'Combined'}
        strategy_name = strategy_map.get(strategy_choice, 'Combined')
        
        paper_trading_session(symbols, strategy_name)
    
    elif choice == '4':
        print("\nLive trading requires Zerodha API setup.")
        print("Please configure your API credentials in .env file first.")
        print("Feature coming soon!")
    
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nError: {e}")
