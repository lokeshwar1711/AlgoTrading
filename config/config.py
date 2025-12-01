import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the trading system"""
    
    # Project Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    HISTORICAL_DATA_DIR = DATA_DIR / "historical"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Zerodha Kite API
    KITE_API_KEY = os.getenv("KITE_API_KEY", "")
    KITE_API_SECRET = os.getenv("KITE_API_SECRET", "")
    KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN", "")
    
    # Trading Configuration
    TRADING_MODE = os.getenv("TRADING_MODE", "paper")  # paper or live
    CAPITAL = float(os.getenv("CAPITAL", 100000))
    
    # Risk Management
    MAX_RISK_PER_TRADE = float(os.getenv("MAX_RISK_PER_TRADE", 2))
    MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 5))
    MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", 5))
    
    # Data Configuration
    DATA_SOURCE = os.getenv("DATA_SOURCE", "yfinance")
    HISTORICAL_DATA_DAYS = int(os.getenv("HISTORICAL_DATA_DAYS", 365))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/trading.db")
    
    # Market Hours (IST)
    MARKET_OPEN_HOUR = 9
    MARKET_OPEN_MINUTE = 15
    MARKET_CLOSE_HOUR = 15
    MARKET_CLOSE_MINUTE = 30
    
    # Technical Indicators Default Periods
    TECHNICAL_INDICATORS = {
        'sma_short': 20,
        'sma_long': 50,
        'ema_short': 12,
        'ema_long': 26,
        'rsi_period': 14,
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        'bb_period': 20,
        'bb_std': 2,
        'atr_period': 14,
        'adx_period': 14,
    }
    
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if cls.TRADING_MODE == "live":
            if not cls.KITE_API_KEY or not cls.KITE_API_SECRET:
                raise ValueError("Kite API credentials are required for live trading")
        
        # Create directories if they don't exist
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.HISTORICAL_DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        
        return True

config = Config()
