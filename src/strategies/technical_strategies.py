"""
Moving Average Crossover Strategy
Simple strategy based on SMA/EMA crossovers
"""

import pandas as pd
import numpy as np
from src.strategies.base_strategy import BaseStrategy
from config.config import config


class MovingAverageCrossover(BaseStrategy):
    """Moving Average Crossover Strategy"""
    
    def __init__(self, short_window=20, long_window=50, ma_type='SMA'):
        """
        Initialize MA Crossover strategy
        
        Args:
            short_window: Period for short moving average
            long_window: Period for long moving average
            ma_type: Type of MA ('SMA' or 'EMA')
        """
        super().__init__(name=f"MA_Crossover_{ma_type}_{short_window}_{long_window}")
        self.short_window = short_window
        self.long_window = long_window
        self.ma_type = ma_type
    
    def calculate_indicators(self, df):
        """Calculate moving averages"""
        df = df.copy()
        
        if self.ma_type == 'SMA':
            df['ma_short'] = df['close'].rolling(window=self.short_window).mean()
            df['ma_long'] = df['close'].rolling(window=self.long_window).mean()
        elif self.ma_type == 'EMA':
            df['ma_short'] = df['close'].ewm(span=self.short_window, adjust=False).mean()
            df['ma_long'] = df['close'].ewm(span=self.long_window, adjust=False).mean()
        
        return df
    
    def generate_signals(self, df):
        """Generate buy/sell signals"""
        df = df.copy()
        df['signal'] = 0
        
        # Buy when short MA crosses above long MA
        df.loc[(df['ma_short'] > df['ma_long']) & 
               (df['ma_short'].shift(1) <= df['ma_long'].shift(1)), 'signal'] = 1
        
        # Sell when short MA crosses below long MA
        df.loc[(df['ma_short'] < df['ma_long']) & 
               (df['ma_short'].shift(1) >= df['ma_long'].shift(1)), 'signal'] = -1
        
        return df


class RSIStrategy(BaseStrategy):
    """RSI-based trading strategy"""
    
    def __init__(self, period=14, oversold=30, overbought=70):
        """
        Initialize RSI strategy
        
        Args:
            period: RSI period
            oversold: Oversold threshold (buy signal)
            overbought: Overbought threshold (sell signal)
        """
        super().__init__(name=f"RSI_{period}_{oversold}_{overbought}")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_indicators(self, df):
        """Calculate RSI"""
        df = df.copy()
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        return df
    
    def generate_signals(self, df):
        """Generate buy/sell signals"""
        df = df.copy()
        df['signal'] = 0
        
        # Buy when RSI crosses above oversold level
        df.loc[(df['rsi'] > self.oversold) & 
               (df['rsi'].shift(1) <= self.oversold), 'signal'] = 1
        
        # Sell when RSI crosses below overbought level
        df.loc[(df['rsi'] < self.overbought) & 
               (df['rsi'].shift(1) >= self.overbought), 'signal'] = -1
        
        return df


class MACDStrategy(BaseStrategy):
    """MACD-based trading strategy"""
    
    def __init__(self, fast=12, slow=26, signal=9):
        """
        Initialize MACD strategy
        
        Args:
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
        """
        super().__init__(name=f"MACD_{fast}_{slow}_{signal}")
        self.fast = fast
        self.slow = slow
        self.signal_period = signal
    
    def calculate_indicators(self, df):
        """Calculate MACD"""
        df = df.copy()
        
        ema_fast = df['close'].ewm(span=self.fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.slow, adjust=False).mean()
        
        df['macd'] = ema_fast - ema_slow
        df['macd_signal'] = df['macd'].ewm(span=self.signal_period, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        return df
    
    def generate_signals(self, df):
        """Generate buy/sell signals"""
        df = df.copy()
        df['signal'] = 0
        
        # Buy when MACD crosses above signal line
        df.loc[(df['macd'] > df['macd_signal']) & 
               (df['macd'].shift(1) <= df['macd_signal'].shift(1)), 'signal'] = 1
        
        # Sell when MACD crosses below signal line
        df.loc[(df['macd'] < df['macd_signal']) & 
               (df['macd'].shift(1) >= df['macd_signal'].shift(1)), 'signal'] = -1
        
        return df


class BollingerBandsStrategy(BaseStrategy):
    """Bollinger Bands trading strategy"""
    
    def __init__(self, period=20, std_dev=2):
        """
        Initialize Bollinger Bands strategy
        
        Args:
            period: Moving average period
            std_dev: Standard deviation multiplier
        """
        super().__init__(name=f"BB_{period}_{std_dev}")
        self.period = period
        self.std_dev = std_dev
    
    def calculate_indicators(self, df):
        """Calculate Bollinger Bands"""
        df = df.copy()
        
        df['bb_middle'] = df['close'].rolling(window=self.period).mean()
        df['bb_std'] = df['close'].rolling(window=self.period).std()
        df['bb_upper'] = df['bb_middle'] + (self.std_dev * df['bb_std'])
        df['bb_lower'] = df['bb_middle'] - (self.std_dev * df['bb_std'])
        
        return df
    
    def generate_signals(self, df):
        """Generate buy/sell signals"""
        df = df.copy()
        df['signal'] = 0
        
        # Buy when price crosses above lower band
        df.loc[(df['close'] > df['bb_lower']) & 
               (df['close'].shift(1) <= df['bb_lower'].shift(1)), 'signal'] = 1
        
        # Sell when price crosses below upper band
        df.loc[(df['close'] < df['bb_upper']) & 
               (df['close'].shift(1) >= df['bb_upper'].shift(1)), 'signal'] = -1
        
        return df


class CombinedStrategy(BaseStrategy):
    """Combined multi-indicator strategy"""
    
    def __init__(self):
        """Initialize combined strategy"""
        super().__init__(name="Combined_Strategy")
        self.ma_short = config.TECHNICAL_INDICATORS['sma_short']
        self.ma_long = config.TECHNICAL_INDICATORS['sma_long']
        self.rsi_period = config.TECHNICAL_INDICATORS['rsi_period']
    
    def calculate_indicators(self, df):
        """Calculate multiple indicators"""
        df = df.copy()
        
        # Moving averages
        df['ma_short'] = df['close'].rolling(window=self.ma_short).mean()
        df['ma_long'] = df['close'].rolling(window=self.ma_long).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = df['close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        return df
    
    def generate_signals(self, df):
        """Generate signals using multiple conditions"""
        df = df.copy()
        df['signal'] = 0
        
        # Buy conditions: MA crossover + RSI oversold + MACD positive
        buy_condition = (
            (df['ma_short'] > df['ma_long']) &
            (df['rsi'] < 50) &
            (df['macd'] > df['macd_signal'])
        )
        
        # Sell conditions: MA crossover + RSI overbought + MACD negative
        sell_condition = (
            (df['ma_short'] < df['ma_long']) &
            (df['rsi'] > 50) &
            (df['macd'] < df['macd_signal'])
        )
        
        df.loc[buy_condition, 'signal'] = 1
        df.loc[sell_condition, 'signal'] = -1
        
        return df
