"""
Configuration Manager for Pig3on
"""

import os
import json
import socket
from pathlib import Path

class Config:
    VERSION = "1.0.0"
    
    def __init__(self):
        self.version = self.VERSION
        self.config_dir = Path.home() / '.pig3on'
        self.config_file = self.config_dir / 'config.json'
        self.download_dir = Path.home() / 'Downloads' / 'Pig3on'
        
        # Network settings
        self.discovery_port = 37777
        self.transfer_port = 37778
        
        # Device settings
        self.device_name = self._get_device_name()
        
        # Load config if exists
        if self.config_file.exists():
            self.load()
    
    def _get_device_name(self):
        """Get device hostname"""
        try:
            return socket.gethostname()
        except:
            return "Unknown-Device"
    
    def initialize(self):
        """Initialize configuration"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.save()
    
    def is_initialized(self):
        """Check if config is initialized"""
        return self.config_file.exists()
    
    def save(self):
        """Save configuration to file"""
        config_data = {
            'version': self.version,
            'device_name': self.device_name,
            'discovery_port': self.discovery_port,
            'transfer_port': self.transfer_port,
            'download_dir': str(self.download_dir)
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def load(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            self.device_name = config_data.get('device_name', self.device_name)
            self.discovery_port = config_data.get('discovery_port', self.discovery_port)
            self.transfer_port = config_data.get('transfer_port', self.transfer_port)
            self.download_dir = Path(config_data.get('download_dir', self.download_dir))
            
        except Exception as e:
            print(f"Failed to load config: {e}")
    
    def update(self, **kwargs):
        """Update configuration"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()