"""
Data Handler for fetching market data from multiple sources
"""

import pandas as pd
import yfinance as yf
from nsepy import get_history
from datetime import datetime, timedelta
from src.utils.logger import get_logger
from config.config import config

logger = get_logger(__name__)


class DataHandler:
    """Handles data fetching from multiple sources"""
    
    def __init__(self, data_source="yfinance"):
        """
        Initialize data handler
        
        Args:
            data_source: Data source (yfinance, nsepy, kite)
        """
        self.data_source = data_source
        logger.info(f"DataHandler initialized with source: {data_source}")
    
    def get_historical_data(self, symbol, start_date=None, end_date=None, interval="1d"):
        """
        Get historical data for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'TCS')
            start_date: Start date (datetime or string)
            end_date: End date (datetime or string)
            interval: Data interval (1d, 1h, 15m, etc.)
            
        Returns:
            pd.DataFrame: Historical data with OHLCV
        """
        if end_date is None:
            end_date = datetime.now()
        
        if start_date is None:
            start_date = end_date - timedelta(days=config.HISTORICAL_DATA_DAYS)
        
        try:
            if self.data_source == "yfinance":
                return self._fetch_from_yfinance(symbol, start_date, end_date, interval)
            elif self.data_source == "nsepy":
                return self._fetch_from_nsepy(symbol, start_date, end_date)
            else:
                logger.error(f"Unknown data source: {self.data_source}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _fetch_from_yfinance(self, symbol, start_date, end_date, interval):
        """Fetch data from Yahoo Finance"""
        # Add .NS suffix for NSE stocks if not present
        if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
            symbol = f"{symbol}.NS"
        
        logger.info(f"Fetching data for {symbol} from yfinance")
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        
        if df.empty:
            logger.warning(f"No data found for {symbol}")
            return pd.DataFrame()
        
        # Standardize column names
        df.columns = [col.lower() for col in df.columns]
        df.index.name = 'date'
        df.reset_index(inplace=True)
        
        logger.info(f"Fetched {len(df)} records for {symbol}")
        return df
    
    def _fetch_from_nsepy(self, symbol, start_date, end_date):
        """Fetch data from NSEpy"""
        logger.info(f"Fetching data for {symbol} from nsepy")
        
        try:
            df = get_history(
                symbol=symbol,
                start=start_date,
                end=end_date
            )
            
            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()
            
            # Standardize column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            df.index.name = 'date'
            df.reset_index(inplace=True)
            
            logger.info(f"Fetched {len(df)} records for {symbol}")
            return df
        except Exception as e:
            logger.error(f"NSEpy fetch failed: {e}")
            return pd.DataFrame()
    
    def get_multiple_stocks(self, symbols, start_date=None, end_date=None):
        """
        Get historical data for multiple symbols
        
        Args:
            symbols: List of stock symbols
            start_date: Start date
            end_date: End date
            
        Returns:
            dict: Dictionary with symbol as key and DataFrame as value
        """
        data = {}
        for symbol in symbols:
            logger.info(f"Fetching data for {symbol}")
            df = self.get_historical_data(symbol, start_date, end_date)
            if not df.empty:
                data[symbol] = df
        
        return data
    
    def save_data(self, df, symbol, format='csv'):
        """
        Save data to file
        
        Args:
            df: DataFrame to save
            symbol: Stock symbol
            format: File format (csv, pickle)
        """
        filename = config.HISTORICAL_DATA_DIR / f"{symbol}_{datetime.now().strftime('%Y%m%d')}"
        
        try:
            if format == 'csv':
                df.to_csv(f"{filename}.csv", index=False)
            elif format == 'pickle':
                df.to_pickle(f"{filename}.pkl")
            
            logger.info(f"Data saved to {filename}.{format}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    def load_data(self, symbol, date=None, format='csv'):
        """
        Load data from file
        
        Args:
            symbol: Stock symbol
            date: Date string (YYYYMMDD), if None uses today
            format: File format (csv, pickle)
            
        Returns:
            pd.DataFrame: Loaded data
        """
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        filename = config.HISTORICAL_DATA_DIR / f"{symbol}_{date}"
        
        try:
            if format == 'csv':
                df = pd.read_csv(f"{filename}.csv")
            elif format == 'pickle':
                df = pd.read_pickle(f"{filename}.pkl")
            
            logger.info(f"Data loaded from {filename}.{format}")
            return df
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return pd.DataFrame()
    
    def get_nifty_50_stocks(self):
        """Get list of Nifty 50 stocks"""
        # Top Nifty 50 stocks (you can update this list)
        nifty_50 = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
            'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
            'BAJFINANCE', 'LT', 'ASIANPAINT', 'HCLTECH', 'AXISBANK',
            'MARUTI', 'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'NESTLEIND',
            'WIPRO', 'TECHM', 'NTPC', 'POWERGRID', 'ONGC',
            'TATAMOTORS', 'TATASTEEL', 'M&M', 'BAJAJFINSV', 'ADANIPORTS',
            'INDUSINDBK', 'CIPLA', 'DRREDDY', 'JSWSTEEL', 'GRASIM',
            'HINDALCO', 'BRITANNIA', 'COALINDIA', 'DIVISLAB', 'EICHERMOT',
            'HEROMOTOCO', 'SHREECEM', 'SBILIFE', 'BPCL', 'UPL',
            'APOLLOHOSP', 'BAJAJ-AUTO', 'TATACONSUM', 'HDFCLIFE', 'ADANIENT'
        ]
        return nifty_50
    
    def get_bank_nifty_stocks(self):
        """Get list of Bank Nifty stocks"""
        bank_nifty = [
            'HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK',
            'INDUSINDBK', 'BANKBARODA', 'PNB', 'AUBANK', 'BANDHANBNK',
            'FEDERALBNK', 'IDFCFIRSTB'
        ]
        return bank_nifty
