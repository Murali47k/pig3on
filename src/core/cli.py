"""
CLI Command Handler for Pig3on
"""

import argparse
import sys
from pathlib import Path
from .connection import ConnectionManager
from .transfer import FileTransfer
from utils.logger import get_logger

logger = get_logger(__name__)

class CLI:
    def __init__(self, config):
        self.config = config
        self.connection_manager = ConnectionManager(config)
        self.file_transfer = FileTransfer(config, self.connection_manager)
        
    def execute(self, args):
        """Execute CLI commands"""
        if not args:
            self.print_help()
            return
        
        command = args[0].lower()
        
        if command == "connect":
            self.handle_connect(args[1:])
        elif command == "send":
            self.handle_send(args[1:])
        elif command == "receive":
            self.handle_receive(args[1:])
        elif command == "disconnect":
            self.handle_disconnect()
        elif command == "status":
            self.handle_status()
        elif command == "help" or command == "-h" or command == "--help":
            self.print_help()
        else:
            logger.error(f"Unknown command: {command}")
            self.print_help()
    
    def handle_connect(self, args):
        """Handle connection command"""
        logger.info("🔍 Searching for nearby Pig3on devices...")
        
        # Scan for devices
        devices = self.connection_manager.scan_devices()
        
        if not devices:
            logger.warning("No devices found. Make sure the other device is running Pig3on.")
            return
        
        logger.info(f"\n📱 Found {len(devices)} device(s):")
        for i, device in enumerate(devices, 1):
            logger.info(f"  {i}. {device['name']} ({device['address']})")
        
        # Auto-connect if only one device
        if len(devices) == 1:
            device = devices[0]
        else:
            try:
                choice = int(input("\nSelect device number: ")) - 1
                if choice < 0 or choice >= len(devices):
                    logger.error("Invalid selection")
                    return
                device = devices[choice]
            except (ValueError, KeyboardInterrupt):
                logger.error("Invalid input")
                return
        
        # Attempt connection
        logger.info(f"\n🔗 Connecting to {device['name']}...")
        if self.connection_manager.connect(device):
            logger.info("✅ Successfully paired and connected!")
        else:
            logger.error("❌ Connection failed")
    
    def handle_send(self, args):
        """Handle file send command"""
        if not args:
            logger.error("Usage: pig3on send <file_path>")
            return
        
        file_path = Path(args[0])
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        if not self.connection_manager.is_connected():
            logger.error("Not connected to any device. Use 'pig3on connect' first.")
            return
        
        logger.info(f"📤 Sending: {file_path.name}")
        
        if self.file_transfer.send_file(file_path):
            logger.info("✅ File sent successfully!")
        else:
            logger.error("❌ File transfer failed")
    
    def handle_receive(self, args):
        """Handle receive mode"""
        logger.info("📥 Listening for incoming files...")
        logger.info("Press Ctrl+C to stop\n")
        
        self.connection_manager.start_listening()
    
    def handle_disconnect(self):
        """Handle disconnect command"""
        if self.connection_manager.disconnect():
            logger.info("✅ Disconnected")
        else:
            logger.warning("Not connected to any device")
    
    def handle_status(self):
        """Show connection status"""
        status = self.connection_manager.get_status()
        
        logger.info("\n📊 Pig3on Status")
        logger.info("=" * 40)
        logger.info(f"Device Name: {status['device_name']}")
        logger.info(f"Connected: {'Yes' if status['connected'] else 'No'}")
        
        if status['connected']:
            logger.info(f"Peer: {status['peer_name']}")
            logger.info(f"Connection Type: {status['connection_type']}")
        
        logger.info("=" * 40)
    
    def print_help(self):
        """Print help message"""
        help_text = """
🕊️  Pig3on - P2P File Transfer System

USAGE:
    pig3on <command> [arguments]

COMMANDS:
    connect                 Scan and connect to nearby devices
    send <file>            Send a file to connected device
    receive                Start listening for incoming files
    disconnect             Disconnect from current peer
    status                 Show connection status
    help                   Show this help message

EXAMPLES:
    pig3on connect
    pig3on send document.pdf
    pig3on send image.png
    pig3on receive
    pig3on disconnect

NOTES:
    - Both devices must have Pig3on installed
    - Ensure WiFi/Bluetooth is enabled
    - Files are transferred in encrypted packets
        """
        print(help_text)