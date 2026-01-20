"""
Connection Manager for Pig3on
Handles WiFi and Bluetooth connections
"""

import socket
import threading
import time
import json
from pathlib import Path
from utils.logger import get_logger
from utils.crypto import CryptoHelper

logger = get_logger(__name__)

class ConnectionManager:
    def __init__(self, config):
        self.config = config
        self.crypto = CryptoHelper()
        self.socket = None
        self.server_socket = None
        self.connected = False
        self.peer_info = None
        self.connection_type = None
        self.listening = False
        self._listen_thread = None
        
    def scan_devices(self, timeout=5):
        """Scan for nearby Pig3on devices using UDP broadcast"""
        devices = []
        
        try:
            # Create UDP socket for broadcasting
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            scan_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            scan_socket.settimeout(1)
            
            # Broadcast discovery message
            message = json.dumps({
                'type': 'DISCOVER',
                'name': self.config.device_name,
                'version': self.config.version
            }).encode()
            
            scan_socket.sendto(message, ('<broadcast>', self.config.discovery_port))
            
            # Listen for responses
            start_time = time.time()
            seen_addresses = set()
            
            while time.time() - start_time < timeout:
                try:
                    data, addr = scan_socket.recvfrom(1024)
                    
                    if addr[0] not in seen_addresses:
                        response = json.loads(data.decode())
                        
                        if response.get('type') == 'DISCOVER_RESPONSE':
                            devices.append({
                                'name': response.get('name', 'Unknown'),
                                'address': addr[0],
                                'port': response.get('port', self.config.transfer_port)
                            })
                            seen_addresses.add(addr[0])
                            
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.debug(f"Scan error: {e}")
                    
            scan_socket.close()
            
        except Exception as e:
            logger.error(f"Device scan failed: {e}")
        
        return devices
    
    def start_listening(self):
        """Start listening for connections"""
        if self.listening:
            logger.warning("Already listening")
            return
        
        self.listening = True
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()
        
        try:
            while self.listening:
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.listening = False
            logger.info("\nStopped listening")
    
    def _listen_loop(self):
        """Background listening loop"""
        # Start discovery responder
        discovery_thread = threading.Thread(target=self._discovery_responder, daemon=True)
        discovery_thread.start()
        
        # Start connection listener
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.config.transfer_port))
            self.server_socket.listen(1)
            self.server_socket.settimeout(1)
            
            logger.info(f"Listening on port {self.config.transfer_port}")
            
            while self.listening:
                try:
                    client_socket, addr = self.server_socket.accept()
                    logger.info(f"\n📞 Incoming connection from {addr[0]}")
                    
                    # Request pairing confirmation
                    response = input("Accept connection? (yes/no): ").lower()
                    
                    if response in ['yes', 'y']:
                        client_socket.send(b'ACCEPT')
                        self.socket = client_socket
                        self.connected = True
                        self.peer_info = {'address': addr[0]}
                        self.connection_type = 'WiFi'
                        logger.info("✅ Paired successfully!")
                        
                        # Handle incoming transfers
                        self._handle_incoming_transfers()
                    else:
                        client_socket.send(b'REJECT')
                        client_socket.close()
                        logger.info("Connection rejected")
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.listening:
                        logger.error(f"Listen error: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to start listener: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def _discovery_responder(self):
        """Respond to discovery broadcasts"""
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.bind(('', self.config.discovery_port))
            udp_socket.settimeout(1)
            
            while self.listening:
                try:
                    data, addr = udp_socket.recvfrom(1024)
                    message = json.loads(data.decode())
                    
                    if message.get('type') == 'DISCOVER':
                        response = json.dumps({
                            'type': 'DISCOVER_RESPONSE',
                            'name': self.config.device_name,
                            'port': self.config.transfer_port,
                            'version': self.config.version
                        }).encode()
                        
                        udp_socket.sendto(response, addr)
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.debug(f"Discovery responder error: {e}")
                    
            udp_socket.close()
            
        except Exception as e:
            logger.error(f"Discovery responder failed: {e}")
    
    def connect(self, device):
        """Connect to a device"""
        try:
            # Create TCP connection
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            
            logger.info(f"Connecting to {device['address']}:{device['port']}...")
            self.socket.connect((device['address'], device['port']))
            
            # Wait for pairing response
            response = self.socket.recv(1024).decode()
            
            if response == 'ACCEPT':
                self.connected = True
                self.peer_info = device
                self.connection_type = 'WiFi'
                return True
            else:
                logger.warning("Connection rejected by peer")
                self.socket.close()
                return False
                
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            if self.socket:
                self.socket.close()
            return False
    
    def _handle_incoming_transfers(self):
        """Handle incoming file transfers"""
        from .transfer import FileTransfer
        transfer = FileTransfer(self.config, self)
        
        while self.connected:
            try:
                if not transfer.receive_file():
                    break
            except Exception as e:
                logger.error(f"Transfer error: {e}")
                break
    
    def disconnect(self):
        """Disconnect from peer"""
        if not self.connected:
            return False
        
        try:
            if self.socket:
                self.socket.close()
            self.connected = False
            self.peer_info = None
            self.connection_type = None
            return True
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
            return False
    
    def is_connected(self):
        """Check if connected"""
        return self.connected
    
    def get_status(self):
        """Get connection status"""
        return {
            'device_name': self.config.device_name,
            'connected': self.connected,
            'peer_name': self.peer_info.get('name', 'Unknown') if self.peer_info else None,
            'connection_type': self.connection_type
        }