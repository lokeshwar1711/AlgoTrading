"""
Backtesting Engine
Comprehensive backtesting with performance metrics and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Backtester:
    """Backtesting engine for trading strategies"""
    
    def __init__(self, strategy, initial_capital=100000):
        """
        Initialize backtester
        
        Args:
            strategy: Strategy instance
            initial_capital: Starting capital
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.results = None
        
        logger.info(f"Backtester initialized with {strategy.name}")
    
    def run(self, df, commission=0.001):
        """
        Run backtest on historical data
        
        Args:
            df: DataFrame with OHLCV data
            commission: Commission per trade (0.001 = 0.1%)
            
        Returns:
            dict: Backtest results
        """
        logger.info(f"Running backtest on {len(df)} data points")
        
        # Calculate indicators and generate signals
        df = self.strategy.calculate_indicators(df)
        df = self.strategy.generate_signals(df)
        
        # Initialize portfolio
        capital = self.initial_capital
        position = 0
        position_value = 0
        trades = []
        portfolio_values = []
        
        for i in range(len(df)):
            current_price = df['close'].iloc[i]
            signal = df['signal'].iloc[i] if 'signal' in df.columns else 0
            
            # Calculate current portfolio value
            portfolio_value = capital + (position * current_price)
            portfolio_values.append(portfolio_value)
            
            # Execute trades based on signals
            if signal == 1 and position == 0:  # Buy signal
                # Buy with available capital
                position = (capital * 0.95) / current_price  # Keep 5% cash
                position_value = position * current_price
                capital -= position_value
                capital -= position_value * commission  # Commission
                
                trades.append({
                    'type': 'BUY',
                    'date': df['date'].iloc[i] if 'date' in df.columns else i,
                    'price': current_price,
                    'quantity': position,
                    'value': position_value
                })
                
                logger.debug(f"BUY: {position:.2f} @ ₹{current_price:.2f}")
                
            elif signal == -1 and position > 0:  # Sell signal
                # Sell entire position
                sell_value = position * current_price
                capital += sell_value
                capital -= sell_value * commission  # Commission
                
                pnl = sell_value - position_value
                
                trades.append({
                    'type': 'SELL',
                    'date': df['date'].iloc[i] if 'date' in df.columns else i,
                    'price': current_price,
                    'quantity': position,
                    'value': sell_value,
                    'pnl': pnl
                })
                
                logger.debug(f"SELL: {position:.2f} @ ₹{current_price:.2f}, PnL: ₹{pnl:.2f}")
                
                position = 0
                position_value = 0
        
        # Close any open position at the end
        if position > 0:
            final_value = position * df['close'].iloc[-1]
            capital += final_value
            capital -= final_value * commission
            
            pnl = final_value - position_value
            trades.append({
                'type': 'SELL',
                'date': df['date'].iloc[-1] if 'date' in df.columns else len(df)-1,
                'price': df['close'].iloc[-1],
                'quantity': position,
                'value': final_value,
                'pnl': pnl
            })
        
        # Calculate performance metrics
        final_capital = capital
        total_return = ((final_capital - self.initial_capital) / self.initial_capital) * 100
        
        # Calculate more metrics
        buy_trades = [t for t in trades if t['type'] == 'BUY']
        sell_trades = [t for t in trades if t['type'] == 'SELL']
        
        winning_trades = [t for t in sell_trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in sell_trades if t.get('pnl', 0) < 0]
        
        win_rate = (len(winning_trades) / len(sell_trades) * 100) if sell_trades else 0
        
        avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0
        
        # Calculate max drawdown
        portfolio_series = pd.Series(portfolio_values)
        cumulative_max = portfolio_series.cummax()
        drawdown = (portfolio_series - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min() * 100
        
        # Calculate Sharpe ratio (assuming 252 trading days, 5% risk-free rate)
        returns = portfolio_series.pct_change().dropna()
        excess_returns = returns - (0.05 / 252)
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns.std() if len(returns) > 0 else 0
        
        self.results = {
            'strategy': self.strategy.name,
            'initial_capital': self.initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'total_trades': len(buy_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'trades': trades,
            'portfolio_values': portfolio_values
        }
        
        logger.info(f"Backtest complete: Return = {total_return:.2f}%, "
                   f"Sharpe = {sharpe_ratio:.2f}, Max DD = {max_drawdown:.2f}%")
        
        return self.results
    
    def print_summary(self):
        """Print backtest summary"""
        if not self.results:
            logger.warning("No results available. Run backtest first.")
            return
        
        print("\n" + "="*60)
        print(f"BACKTEST RESULTS: {self.results['strategy']}")
        print("="*60)
        print(f"Initial Capital:    ₹{self.results['initial_capital']:,.2f}")
        print(f"Final Capital:      ₹{self.results['final_capital']:,.2f}")
        print(f"Total Return:       {self.results['total_return']:.2f}%")
        print(f"Total Trades:       {self.results['total_trades']}")
        print(f"Winning Trades:     {self.results['winning_trades']}")
        print(f"Losing Trades:      {self.results['losing_trades']}")
        print(f"Win Rate:           {self.results['win_rate']:.2f}%")
        print(f"Average Win:        ₹{self.results['avg_win']:,.2f}")
        print(f"Average Loss:       ₹{self.results['avg_loss']:,.2f}")
        print(f"Max Drawdown:       {self.results['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio:       {self.results['sharpe_ratio']:.2f}")
        print("="*60 + "\n")
    
    def plot_results(self, df, save_path=None):
        """
        Plot backtest results
        
        Args:
            df: Original DataFrame with price data
            save_path: Path to save the plot
        """
        if not self.results:
            logger.warning("No results available. Run backtest first.")
            return
        
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        
        # Plot 1: Price and signals
        df = self.strategy.calculate_indicators(df)
        df = self.strategy.generate_signals(df)
        
        axes[0].plot(df.index, df['close'], label='Close Price', linewidth=1)
        
        buy_signals = df[df['signal'] == 1]
        sell_signals = df[df['signal'] == -1]
        
        axes[0].scatter(buy_signals.index, buy_signals['close'], 
                       marker='^', color='g', s=100, label='Buy Signal')
        axes[0].scatter(sell_signals.index, sell_signals['close'], 
                       marker='v', color='r', s=100, label='Sell Signal')
        
        axes[0].set_title(f'{self.strategy.name} - Trading Signals')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Price (₹)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Portfolio value
        axes[1].plot(self.results['portfolio_values'], linewidth=2, color='blue')
        axes[1].axhline(y=self.initial_capital, color='r', linestyle='--', 
                       label='Initial Capital', alpha=0.7)
        axes[1].set_title('Portfolio Value Over Time')
        axes[1].set_xlabel('Time Period')
        axes[1].set_ylabel('Portfolio Value (₹)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Drawdown
        portfolio_series = pd.Series(self.results['portfolio_values'])
        cumulative_max = portfolio_series.cummax()
        drawdown = (portfolio_series - cumulative_max) / cumulative_max * 100
        
        axes[2].fill_between(range(len(drawdown)), drawdown, 0, 
                            color='red', alpha=0.3)
        axes[2].plot(drawdown, color='red', linewidth=1)
        axes[2].set_title('Drawdown')
        axes[2].set_xlabel('Time Period')
        axes[2].set_ylabel('Drawdown (%)')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        
        plt.show()
    
    def get_trade_log(self):
        """
        Get detailed trade log
        
        Returns:
            pd.DataFrame: Trade log
        """
        if not self.results or not self.results['trades']:
            return pd.DataFrame()
        
        return pd.DataFrame(self.results['trades'])
