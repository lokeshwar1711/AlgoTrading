"""
Risk Management Module
Handles position sizing, stop loss, take profit, and risk controls
"""

from config.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RiskManager:
    """Manages risk for trading positions"""
    
    def __init__(self, capital=None):
        """
        Initialize risk manager
        
        Args:
            capital: Trading capital (uses config if not provided)
        """
        self.capital = capital or config.CAPITAL
        self.max_risk_per_trade = config.MAX_RISK_PER_TRADE
        self.max_daily_loss = config.MAX_DAILY_LOSS
        self.max_open_positions = config.MAX_OPEN_POSITIONS
        self.daily_pnl = 0
        self.open_positions = 0
        
        logger.info(f"RiskManager initialized with capital: ₹{self.capital:,.2f}")
    
    def calculate_position_size(self, entry_price, stop_loss_price, risk_percentage=None):
        """
        Calculate position size based on risk percentage
        
        Args:
            entry_price: Entry price for the trade
            stop_loss_price: Stop loss price
            risk_percentage: Risk per trade (% of capital)
            
        Returns:
            int: Quantity to trade
        """
        if risk_percentage is None:
            risk_percentage = self.max_risk_per_trade
        
        risk_amount = self.capital * (risk_percentage / 100)
        price_risk = abs(entry_price - stop_loss_price)
        
        if price_risk == 0:
            logger.warning("Price risk is zero, cannot calculate position size")
            return 0
        
        quantity = int(risk_amount / price_risk)
        
        logger.info(f"Position size calculated: {quantity} units at ₹{entry_price:.2f}")
        return quantity
    
    def calculate_stop_loss(self, entry_price, method='percentage', value=2):
        """
        Calculate stop loss price
        
        Args:
            entry_price: Entry price
            method: 'percentage' or 'atr'
            value: Percentage or ATR multiplier
            
        Returns:
            float: Stop loss price
        """
        if method == 'percentage':
            stop_loss = entry_price * (1 - value / 100)
        else:
            # For ATR-based stop loss, value should be ATR * multiplier
            stop_loss = entry_price - value
        
        logger.debug(f"Stop loss calculated: ₹{stop_loss:.2f} for entry ₹{entry_price:.2f}")
        return stop_loss
    
    def calculate_take_profit(self, entry_price, stop_loss_price, reward_ratio=2):
        """
        Calculate take profit price based on risk-reward ratio
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop loss price
            reward_ratio: Risk-reward ratio (e.g., 2 means 2:1)
            
        Returns:
            float: Take profit price
        """
        risk = abs(entry_price - stop_loss_price)
        take_profit = entry_price + (risk * reward_ratio)
        
        logger.debug(f"Take profit calculated: ₹{take_profit:.2f} for entry ₹{entry_price:.2f}")
        return take_profit
    
    def can_open_position(self):
        """
        Check if a new position can be opened
        
        Returns:
            bool: True if position can be opened
        """
        # Check maximum open positions
        if self.open_positions >= self.max_open_positions:
            logger.warning(f"Maximum open positions reached: {self.open_positions}")
            return False
        
        # Check daily loss limit
        daily_loss_percentage = (self.daily_pnl / self.capital) * 100
        if daily_loss_percentage <= -self.max_daily_loss:
            logger.warning(f"Daily loss limit reached: {daily_loss_percentage:.2f}%")
            return False
        
        return True
    
    def update_daily_pnl(self, pnl):
        """
        Update daily P&L
        
        Args:
            pnl: Profit/Loss from closed position
        """
        self.daily_pnl += pnl
        logger.info(f"Daily P&L updated: ₹{self.daily_pnl:.2f}")
    
    def update_capital(self, new_capital):
        """
        Update trading capital
        
        Args:
            new_capital: New capital amount
        """
        self.capital = new_capital
        logger.info(f"Capital updated: ₹{self.capital:,.2f}")
    
    def add_position(self):
        """Increment open position count"""
        self.open_positions += 1
        logger.debug(f"Open positions: {self.open_positions}")
    
    def close_position(self):
        """Decrement open position count"""
        if self.open_positions > 0:
            self.open_positions -= 1
            logger.debug(f"Open positions: {self.open_positions}")
    
    def reset_daily_pnl(self):
        """Reset daily P&L (call at start of day)"""
        self.daily_pnl = 0
        logger.info("Daily P&L reset")
    
    def get_risk_metrics(self):
        """
        Get current risk metrics
        
        Returns:
            dict: Risk metrics
        """
        return {
            'capital': self.capital,
            'daily_pnl': self.daily_pnl,
            'daily_pnl_percentage': (self.daily_pnl / self.capital) * 100,
            'open_positions': self.open_positions,
            'max_open_positions': self.max_open_positions,
            'available_positions': self.max_open_positions - self.open_positions,
            'max_risk_per_trade': self.max_risk_per_trade,
            'max_daily_loss': self.max_daily_loss
        }
    
    def validate_order(self, symbol, quantity, price):
        """
        Validate order before placing
        
        Args:
            symbol: Trading symbol
            quantity: Order quantity
            price: Order price
            
        Returns:
            tuple: (bool, str) - (is_valid, message)
        """
        # Check if position can be opened
        if not self.can_open_position():
            return False, "Cannot open new position due to risk limits"
        
        # Check if order value is within limits
        order_value = quantity * price
        max_order_value = self.capital * 0.3  # Max 30% per trade
        
        if order_value > max_order_value:
            return False, f"Order value ₹{order_value:,.2f} exceeds limit ₹{max_order_value:,.2f}"
        
        # Check minimum order value
        if order_value < 500:  # Minimum ₹500
            return False, "Order value too small (minimum ₹500)"
        
        return True, "Order validated successfully"
