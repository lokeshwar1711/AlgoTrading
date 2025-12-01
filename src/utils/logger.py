"""
Logger utility for the trading system
"""

import logging
import colorlog
from pathlib import Path
from datetime import datetime
from config.config import config


def get_logger(name):
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (usually __name__ of the module)
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    console_format = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = config.LOGS_DIR / f"trading_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    return logger
