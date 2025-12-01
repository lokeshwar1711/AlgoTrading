"""
Helper utility functions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz


def is_market_open():
    """
    Check if Indian market is currently open
    
    Returns:
        bool: True if market is open
    """
    from config.config import config
    
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    
    # Check if weekday (Monday = 0, Sunday = 6)
    if now.weekday() > 4:
        return False
    
    # Check market hours
    market_open = now.replace(
        hour=config.MARKET_OPEN_HOUR, 
        minute=config.MARKET_OPEN_MINUTE, 
        second=0
    )
    market_close = now.replace(
        hour=config.MARKET_CLOSE_HOUR, 
        minute=config.MARKET_CLOSE_MINUTE, 
        second=0
    )
    
    return market_open <= now <= market_close


def get_next_trading_day():
    """
    Get the next trading day
    
    Returns:
        datetime: Next trading day
    """
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    next_day = now + timedelta(days=1)
    
    # Skip weekends
    while next_day.weekday() > 4:
        next_day += timedelta(days=1)
    
    return next_day


def format_currency(amount):
    """
    Format amount in Indian currency format
    
    Args:
        amount: Amount to format
        
    Returns:
        str: Formatted string
    """
    return f"₹{amount:,.2f}"


def calculate_returns(prices):
    """
    Calculate returns from price series
    
    Args:
        prices: Series or list of prices
        
    Returns:
        pd.Series: Returns
    """
    if isinstance(prices, list):
        prices = pd.Series(prices)
    
    return prices.pct_change()


def calculate_sharpe_ratio(returns, risk_free_rate=0.05, periods=252):
    """
    Calculate Sharpe ratio
    
    Args:
        returns: Series of returns
        risk_free_rate: Annual risk-free rate (default 5%)
        periods: Number of periods in a year (252 for daily)
        
    Returns:
        float: Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / periods)
    return np.sqrt(periods) * excess_returns.mean() / returns.std()


def calculate_max_drawdown(prices):
    """
    Calculate maximum drawdown
    
    Args:
        prices: Series or list of prices
        
    Returns:
        float: Maximum drawdown (as decimal)
    """
    if isinstance(prices, list):
        prices = pd.Series(prices)
    
    cumulative_max = prices.cummax()
    drawdown = (prices - cumulative_max) / cumulative_max
    return drawdown.min()


def calculate_cagr(initial_value, final_value, years):
    """
    Calculate Compound Annual Growth Rate
    
    Args:
        initial_value: Starting value
        final_value: Ending value
        years: Number of years
        
    Returns:
        float: CAGR as percentage
    """
    if years == 0 or initial_value == 0:
        return 0
    
    cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
    return cagr


def validate_symbol(symbol):
    """
    Validate and format stock symbol
    
    Args:
        symbol: Stock symbol
        
    Returns:
        str: Formatted symbol
    """
    symbol = symbol.upper().strip()
    
    # Remove .NS or .BO suffix if present
    symbol = symbol.replace('.NS', '').replace('.BO', '')
    
    return symbol


def get_symbol_with_exchange(symbol, exchange='NSE'):
    """
    Get symbol with exchange suffix
    
    Args:
        symbol: Stock symbol
        exchange: Exchange (NSE or BSE)
        
    Returns:
        str: Symbol with exchange suffix
    """
    symbol = validate_symbol(symbol)
    
    if exchange.upper() == 'NSE':
        return f"{symbol}.NS"
    elif exchange.upper() == 'BSE':
        return f"{symbol}.BO"
    else:
        return symbol


def get_trading_days(start_date, end_date):
    """
    Get number of trading days between dates
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        int: Number of trading days
    """
    # Simple approximation: exclude weekends
    days = 0
    current = start_date
    
    while current <= end_date:
        if current.weekday() < 5:  # Monday to Friday
            days += 1
        current += timedelta(days=1)
    
    return days


def split_symbol_exchange(symbol):
    """
    Split symbol and exchange from combined format
    
    Args:
        symbol: Symbol in format "EXCHANGE:SYMBOL" or "SYMBOL.NS"
        
    Returns:
        tuple: (symbol, exchange)
    """
    if ':' in symbol:
        exchange, symbol = symbol.split(':')
        return symbol, exchange
    elif '.NS' in symbol:
        return symbol.replace('.NS', ''), 'NSE'
    elif '.BO' in symbol:
        return symbol.replace('.BO', ''), 'BSE'
    else:
        return symbol, 'NSE'


def calculate_position_value(quantity, price):
    """
    Calculate total position value
    
    Args:
        quantity: Number of shares
        price: Price per share
        
    Returns:
        float: Total value
    """
    return quantity * price


def calculate_pnl(entry_price, exit_price, quantity, transaction_type='BUY'):
    """
    Calculate profit/loss
    
    Args:
        entry_price: Entry price
        exit_price: Exit price
        quantity: Quantity
        transaction_type: BUY or SELL
        
    Returns:
        float: P&L
    """
    if transaction_type.upper() == 'BUY':
        return (exit_price - entry_price) * quantity
    else:
        return (entry_price - exit_price) * quantity


def get_lot_size(symbol, segment='EQUITY'):
    """
    Get lot size for symbol
    Note: This is a simplified version. For options, you need to fetch from Kite API
    
    Args:
        symbol: Trading symbol
        segment: EQUITY, FO, etc.
        
    Returns:
        int: Lot size
    """
    # For equity, lot size is 1
    if segment == 'EQUITY':
        return 1
    
    # For futures/options, this would need to be fetched from API
    # This is a placeholder
    return 1


def round_to_tick_size(price, tick_size=0.05):
    """
    Round price to nearest tick size
    
    Args:
        price: Price to round
        tick_size: Tick size (default 0.05 for most Indian stocks)
        
    Returns:
        float: Rounded price
    """
    return round(price / tick_size) * tick_size


def calculate_brokerage(value, rate=0.0003):
    """
    Calculate brokerage for a trade
    
    Args:
        value: Trade value
        rate: Brokerage rate (default 0.03% for Zerodha equity delivery)
        
    Returns:
        float: Brokerage amount
    """
    # Zerodha charges: 0.03% or ₹20 per order, whichever is lower
    brokerage = value * rate
    return min(brokerage, 20)


def calculate_total_charges(value, brokerage_rate=0.0003):
    """
    Calculate total charges including STT, transaction charges, etc.
    
    Args:
        value: Trade value
        brokerage_rate: Brokerage rate
        
    Returns:
        dict: Breakdown of charges
    """
    brokerage = calculate_brokerage(value, brokerage_rate)
    stt = value * 0.001  # 0.1% on sell side
    transaction_charges = value * 0.00325  # NSE: 0.00325%
    gst = (brokerage + transaction_charges) * 0.18  # 18% GST
    sebi_charges = value * 0.0001  # ₹10 per crore
    stamp_duty = value * 0.00015  # 0.015%
    
    total = brokerage + stt + transaction_charges + gst + sebi_charges + stamp_duty
    
    return {
        'brokerage': brokerage,
        'stt': stt,
        'transaction_charges': transaction_charges,
        'gst': gst,
        'sebi_charges': sebi_charges,
        'stamp_duty': stamp_duty,
        'total': total
    }


def format_percentage(value, decimals=2):
    """
    Format value as percentage
    
    Args:
        value: Value to format
        decimals: Number of decimal places
        
    Returns:
        str: Formatted percentage
    """
    return f"{value:.{decimals}f}%"


def create_summary_table(data, title="Summary"):
    """
    Create a formatted summary table
    
    Args:
        data: Dictionary of data
        title: Table title
        
    Returns:
        str: Formatted table
    """
    width = 60
    output = "\n" + "="*width + "\n"
    output += f"{title.center(width)}\n"
    output += "="*width + "\n"
    
    for key, value in data.items():
        output += f"{key:30} : {str(value):>25}\n"
    
    output += "="*width + "\n"
    
    return output
