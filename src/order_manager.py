"""
Order Manager
Handles order execution for both paper trading and live trading
"""

from datetime import datetime
from src.utils.logger import get_logger
from config.config import config
import json

logger = get_logger(__name__)


class Position:
    """Represents a trading position"""
    
    def __init__(self, symbol, quantity, entry_price, entry_time, 
                 stop_loss=None, take_profit=None, order_id=None):
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.order_id = order_id
        self.status = "OPEN"
        self.exit_price = None
        self.exit_time = None
        self.pnl = 0
    
    def close(self, exit_price, exit_time):
        """Close the position"""
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.pnl = (exit_price - self.entry_price) * self.quantity
        self.status = "CLOSED"
        
    def to_dict(self):
        """Convert position to dictionary"""
        return {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'entry_price': self.entry_price,
            'entry_time': str(self.entry_time),
            'exit_price': self.exit_price,
            'exit_time': str(self.exit_time) if self.exit_time else None,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'status': self.status,
            'pnl': self.pnl,
            'order_id': self.order_id
        }


class OrderManager:
    """Manages order execution and position tracking"""
    
    def __init__(self, broker=None, risk_manager=None):
        """
        Initialize order manager
        
        Args:
            broker: Broker instance for live trading
            risk_manager: Risk manager instance
        """
        self.broker = broker
        self.risk_manager = risk_manager
        self.positions = {}  # symbol -> Position
        self.closed_positions = []
        self.orders = []
        
        logger.info(f"OrderManager initialized in {config.TRADING_MODE} mode")
    
    def place_order(self, symbol, transaction_type, quantity, price=None, 
                    stop_loss=None, take_profit=None, order_type="MARKET"):
        """
        Place a trading order
        
        Args:
            symbol: Trading symbol
            transaction_type: BUY or SELL
            quantity: Quantity to trade
            price: Price (for limit orders)
            stop_loss: Stop loss price
            take_profit: Take profit price
            order_type: MARKET or LIMIT
            
        Returns:
            str: Order ID
        """
        # Validate order with risk manager
        if self.risk_manager and transaction_type == "BUY":
            is_valid, message = self.risk_manager.validate_order(
                symbol, quantity, price or 0
            )
            if not is_valid:
                logger.warning(f"Order validation failed: {message}")
                return None
        
        # Place order
        if config.TRADING_MODE == "paper":
            order_id = self._place_paper_order(
                symbol, transaction_type, quantity, price, 
                stop_loss, take_profit, order_type
            )
        else:
            order_id = self._place_live_order(
                symbol, transaction_type, quantity, price, order_type
            )
        
        # Track order
        self.orders.append({
            'order_id': order_id,
            'symbol': symbol,
            'transaction_type': transaction_type,
            'quantity': quantity,
            'price': price,
            'order_type': order_type,
            'time': datetime.now(),
            'status': 'PLACED'
        })
        
        logger.info(f"Order placed: {order_id} - {transaction_type} {quantity} {symbol}")
        return order_id
    
    def _place_paper_order(self, symbol, transaction_type, quantity, price, 
                          stop_loss, take_profit, order_type):
        """Place a paper trading order"""
        order_id = f"PAPER_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        if transaction_type == "BUY":
            # Open position
            position = Position(
                symbol=symbol,
                quantity=quantity,
                entry_price=price,
                entry_time=datetime.now(),
                stop_loss=stop_loss,
                take_profit=take_profit,
                order_id=order_id
            )
            self.positions[symbol] = position
            
            if self.risk_manager:
                self.risk_manager.add_position()
            
            logger.info(f"[PAPER] Opened position: {symbol} @ ₹{price:.2f}")
            
        elif transaction_type == "SELL":
            # Close position
            if symbol in self.positions:
                position = self.positions[symbol]
                position.close(price, datetime.now())
                
                if self.risk_manager:
                    self.risk_manager.update_daily_pnl(position.pnl)
                    self.risk_manager.close_position()
                
                self.closed_positions.append(position)
                del self.positions[symbol]
                
                logger.info(f"[PAPER] Closed position: {symbol} @ ₹{price:.2f}, "
                          f"P&L: ₹{position.pnl:.2f}")
        
        return order_id
    
    def _place_live_order(self, symbol, transaction_type, quantity, price, order_type):
        """Place a live trading order"""
        if not self.broker:
            logger.error("No broker instance available for live trading")
            return None
        
        try:
            order_id = self.broker.place_order(
                symbol=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                price=price
            )
            return order_id
        except Exception as e:
            logger.error(f"Failed to place live order: {e}")
            return None
    
    def check_stop_loss_take_profit(self, current_prices):
        """
        Check and execute stop loss or take profit
        
        Args:
            current_prices: Dictionary of symbol -> current_price
        """
        for symbol, position in list(self.positions.items()):
            if symbol not in current_prices:
                continue
            
            current_price = current_prices[symbol]
            
            # Check stop loss
            if position.stop_loss and current_price <= position.stop_loss:
                logger.warning(f"Stop loss triggered for {symbol} @ ₹{current_price:.2f}")
                self.place_order(symbol, "SELL", position.quantity, current_price)
            
            # Check take profit
            elif position.take_profit and current_price >= position.take_profit:
                logger.info(f"Take profit triggered for {symbol} @ ₹{current_price:.2f}")
                self.place_order(symbol, "SELL", position.quantity, current_price)
    
    def get_open_positions(self):
        """Get all open positions"""
        return {symbol: pos.to_dict() for symbol, pos in self.positions.items()}
    
    def get_closed_positions(self):
        """Get all closed positions"""
        return [pos.to_dict() for pos in self.closed_positions]
    
    def get_position_pnl(self, symbol, current_price):
        """
        Get unrealized P&L for a position
        
        Args:
            symbol: Trading symbol
            current_price: Current market price
            
        Returns:
            float: Unrealized P&L
        """
        if symbol not in self.positions:
            return 0
        
        position = self.positions[symbol]
        return (current_price - position.entry_price) * position.quantity
    
    def get_total_pnl(self, current_prices=None):
        """
        Get total P&L (realized + unrealized)
        
        Args:
            current_prices: Dictionary of symbol -> current_price
            
        Returns:
            dict: Total P&L breakdown
        """
        realized_pnl = sum(pos.pnl for pos in self.closed_positions)
        unrealized_pnl = 0
        
        if current_prices:
            for symbol, position in self.positions.items():
                if symbol in current_prices:
                    unrealized_pnl += self.get_position_pnl(symbol, current_prices[symbol])
        
        return {
            'realized_pnl': realized_pnl,
            'unrealized_pnl': unrealized_pnl,
            'total_pnl': realized_pnl + unrealized_pnl
        }
    
    def close_all_positions(self, current_prices):
        """
        Close all open positions
        
        Args:
            current_prices: Dictionary of symbol -> current_price
        """
        for symbol in list(self.positions.keys()):
            if symbol in current_prices:
                position = self.positions[symbol]
                self.place_order(
                    symbol, "SELL", position.quantity, current_prices[symbol]
                )
                logger.info(f"Force closed position: {symbol}")
    
    def save_positions(self, filepath):
        """Save positions to file"""
        data = {
            'open_positions': self.get_open_positions(),
            'closed_positions': self.get_closed_positions(),
            'orders': self.orders
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Positions saved to {filepath}")
    
    def load_positions(self, filepath):
        """Load positions from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Positions loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Failed to load positions: {e}")
            return None
