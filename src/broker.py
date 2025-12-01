"""
Zerodha Kite Broker Integration
Handles authentication, order placement, and position management
"""

from kiteconnect import KiteConnect
from config.config import config
from src.utils.logger import get_logger
import pickle
import os
from datetime import datetime

logger = get_logger(__name__)


class ZerodhaBroker:
    """Wrapper class for Zerodha Kite Connect API"""
    
    def __init__(self):
        self.api_key = config.KITE_API_KEY
        self.api_secret = config.KITE_API_SECRET
        self.access_token = config.KITE_ACCESS_TOKEN
        self.kite = None
        
        if config.TRADING_MODE == "live":
            self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize Kite Connect"""
        try:
            self.kite = KiteConnect(api_key=self.api_key)
            
            # If access token exists, use it
            if self.access_token:
                self.kite.set_access_token(self.access_token)
                logger.info("Kite Connect initialized with existing access token")
            else:
                logger.warning("No access token found. Please generate one.")
                
        except Exception as e:
            logger.error(f"Failed to initialize Kite Connect: {e}")
            raise
    
    def generate_session(self, request_token):
        """
        Generate access token using request token
        
        Args:
            request_token: Request token received after login
            
        Returns:
            dict: Session data with access token
        """
        try:
            data = self.kite.generate_session(request_token, api_secret=self.api_secret)
            self.access_token = data["access_token"]
            self.kite.set_access_token(self.access_token)
            
            logger.info("Session generated successfully")
            logger.info(f"Access Token: {self.access_token}")
            logger.info("Please save this token in your .env file")
            
            return data
        except Exception as e:
            logger.error(f"Failed to generate session: {e}")
            raise
    
    def get_login_url(self):
        """Get the login URL for Kite Connect"""
        return self.kite.login_url()
    
    def get_profile(self):
        """Get user profile"""
        try:
            return self.kite.profile()
        except Exception as e:
            logger.error(f"Failed to get profile: {e}")
            return None
    
    def get_instruments(self, exchange="NSE"):
        """
        Get list of instruments
        
        Args:
            exchange: Exchange name (NSE, NFO, BSE, etc.)
            
        Returns:
            list: List of instruments
        """
        try:
            instruments = self.kite.instruments(exchange)
            logger.info(f"Fetched {len(instruments)} instruments from {exchange}")
            return instruments
        except Exception as e:
            logger.error(f"Failed to fetch instruments: {e}")
            return []
    
    def get_quote(self, symbols):
        """
        Get quote for symbols
        
        Args:
            symbols: List of symbols in format "EXCHANGE:SYMBOL"
            
        Returns:
            dict: Quote data
        """
        try:
            return self.kite.quote(symbols)
        except Exception as e:
            logger.error(f"Failed to fetch quote: {e}")
            return {}
    
    def get_historical_data(self, instrument_token, from_date, to_date, interval):
        """
        Get historical data
        
        Args:
            instrument_token: Instrument token
            from_date: From date (datetime)
            to_date: To date (datetime)
            interval: Candle interval (minute, day, 3minute, 5minute, etc.)
            
        Returns:
            list: Historical data
        """
        try:
            return self.kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
        except Exception as e:
            logger.error(f"Failed to fetch historical data: {e}")
            return []
    
    def place_order(self, symbol, transaction_type, quantity, order_type="MARKET", 
                    price=None, product="MIS", exchange="NSE", variety="regular"):
        """
        Place an order
        
        Args:
            symbol: Trading symbol
            transaction_type: BUY or SELL
            quantity: Quantity to trade
            order_type: MARKET, LIMIT, SL, SL-M
            price: Price for limit orders
            product: CNC, MIS, NRML
            exchange: NSE, NFO, BSE
            variety: regular, amo, co, iceberg
            
        Returns:
            str: Order ID
        """
        if config.TRADING_MODE == "paper":
            logger.info(f"[PAPER TRADE] {transaction_type} {quantity} {symbol} @ {order_type}")
            return f"PAPER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            order_id = self.kite.place_order(
                tradingsymbol=symbol,
                exchange=exchange,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                product=product,
                price=price,
                variety=variety
            )
            logger.info(f"Order placed: {order_id}")
            return order_id
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            raise
    
    def modify_order(self, order_id, quantity=None, price=None, order_type=None):
        """Modify an existing order"""
        if config.TRADING_MODE == "paper":
            logger.info(f"[PAPER TRADE] Modified order {order_id}")
            return order_id
        
        try:
            self.kite.modify_order(
                order_id=order_id,
                quantity=quantity,
                price=price,
                order_type=order_type,
                variety="regular"
            )
            logger.info(f"Order modified: {order_id}")
            return order_id
        except Exception as e:
            logger.error(f"Failed to modify order: {e}")
            raise
    
    def cancel_order(self, order_id, variety="regular"):
        """Cancel an order"""
        if config.TRADING_MODE == "paper":
            logger.info(f"[PAPER TRADE] Cancelled order {order_id}")
            return order_id
        
        try:
            self.kite.cancel_order(order_id=order_id, variety=variety)
            logger.info(f"Order cancelled: {order_id}")
            return order_id
        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            raise
    
    def get_orders(self):
        """Get all orders"""
        if config.TRADING_MODE == "paper":
            return []
        
        try:
            return self.kite.orders()
        except Exception as e:
            logger.error(f"Failed to fetch orders: {e}")
            return []
    
    def get_positions(self):
        """Get all positions"""
        if config.TRADING_MODE == "paper":
            return {"net": [], "day": []}
        
        try:
            return self.kite.positions()
        except Exception as e:
            logger.error(f"Failed to fetch positions: {e}")
            return {"net": [], "day": []}
    
    def get_holdings(self):
        """Get all holdings"""
        if config.TRADING_MODE == "paper":
            return []
        
        try:
            return self.kite.holdings()
        except Exception as e:
            logger.error(f"Failed to fetch holdings: {e}")
            return []
    
    def get_margins(self):
        """Get account margins"""
        if config.TRADING_MODE == "paper":
            return {"equity": {"available": {"cash": config.CAPITAL}}}
        
        try:
            return self.kite.margins()
        except Exception as e:
            logger.error(f"Failed to fetch margins: {e}")
            return {}
