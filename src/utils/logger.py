"""
Logging utility for Pig3on
"""

import logging
import sys
from pathlib import Path

# Color codes for terminal
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    FORMATS = {
        logging.DEBUG: Colors.CYAN + '%(message)s' + Colors.RESET,
        logging.INFO: Colors.WHITE + '%(message)s' + Colors.RESET,
        logging.WARNING: Colors.YELLOW + '⚠️  %(message)s' + Colors.RESET,
        logging.ERROR: Colors.RED + '❌ %(message)s' + Colors.RESET,
        logging.CRITICAL: Colors.RED + Colors.BOLD + '❌ %(message)s' + Colors.RESET,
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger():
    """Setup main logger"""
    logger = logging.getLogger('pig3on')
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name):
    """Get logger for module"""
    return logging.getLogger(f'pig3on.{name}')