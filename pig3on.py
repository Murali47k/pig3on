#!/usr/bin/env python3
"""
Pig3on - P2P File Transfer System
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.cli import CLI
from core.config import Config
from utils.logger import setup_logger

def main():
    """Main entry point"""
    # Setup logging
    logger = setup_logger()
    
    # Initialize config
    config = Config()
    
    # Check if pig3on is properly installed
    if not config.is_initialized():
        logger.info("First time setup...")
        config.initialize()
    
    # Initialize CLI
    cli = CLI(config)
    
    # Parse and execute command
    try:
        cli.execute(sys.argv[1:])
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()