"""
Base Strategy Class
All trading strategies should inherit from this class
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""
    
    def __init__(self, name="BaseStrategy"):
        """
        Initialize strategy
        
        Args:
            name: Strategy name
        """
        self.name = name
        self.signals = []
        logger.info(f"Strategy '{self.name}' initialized")
    
    @abstractmethod
    def generate_signals(self, df):
        """
        Generate trading signals based on the strategy
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with added signal column
                         1 = Buy, -1 = Sell, 0 = Hold
        """
        pass
    
    @abstractmethod
    def calculate_indicators(self, df):
        """
        Calculate technical indicators required for the strategy
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with calculated indicators
        """
        pass
    
    def backtest(self, df, initial_capital=100000):
        """
        Simple backtest of the strategy
        
        Args:
            df: DataFrame with OHLCV data
            initial_capital: Starting capital
            
        Returns:
            dict: Backtest results
        """
        df = self.calculate_indicators(df)
        df = self.generate_signals(df)
        
        if 'signal' not in df.columns:
            logger.error("No signal column found in DataFrame")
            return {}
        
        capital = initial_capital
        position = 0
        trades = []
        
        for i in range(len(df)):
            if df['signal'].iloc[i] == 1 and position == 0:  # Buy signal
                position = capital / df['close'].iloc[i]
                entry_price = df['close'].iloc[i]
                trades.append({
                    'type': 'BUY',
                    'date': df['date'].iloc[i] if 'date' in df.columns else i,
                    'price': entry_price,
                    'quantity': position
                })
                logger.debug(f"BUY: {position:.2f} @ {entry_price:.2f}")
                
            elif df['signal'].iloc[i] == -1 and position > 0:  # Sell signal
                exit_price = df['close'].iloc[i]
                capital = position * exit_price
                pnl = capital - initial_capital
                trades.append({
                    'type': 'SELL',
                    'date': df['date'].iloc[i] if 'date' in df.columns else i,
                    'price': exit_price,
                    'quantity': position,
                    'pnl': pnl
                })
                logger.debug(f"SELL: {position:.2f} @ {exit_price:.2f}, PnL: {pnl:.2f}")
                position = 0
        
        # Close any open position at the end
        if position > 0:
            exit_price = df['close'].iloc[-1]
            capital = position * exit_price
        
        total_return = ((capital - initial_capital) / initial_capital) * 100
        
        results = {
            'initial_capital': initial_capital,
            'final_capital': capital,
            'total_return': total_return,
            'total_trades': len([t for t in trades if t['type'] == 'BUY']),
            'trades': trades
        }
        
        logger.info(f"Backtest complete: Return = {total_return:.2f}%")
        return results
    
    def get_current_signal(self, df):
        """
        Get the most recent signal
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            int: Latest signal (1 = Buy, -1 = Sell, 0 = Hold)
        """
        df = self.calculate_indicators(df)
        df = self.generate_signals(df)
        
        if 'signal' not in df.columns or df.empty:
            return 0
        
        return df['signal'].iloc[-1]
    
    def __str__(self):
        return f"Strategy: {self.name}"
