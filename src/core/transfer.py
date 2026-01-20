"""
File Transfer Handler for Pig3on
Handles sending and receiving files with progress tracking
"""

import os
import json
import time
import hashlib
from pathlib import Path
from utils.logger import get_logger
from utils.progress import ProgressBar

logger = get_logger(__name__)

class FileTransfer:
    PACKET_SIZE = 8192  # 8KB packets
    TOTAL_PACKETS = 100  # Split file into 100 packets for progress
    
    def __init__(self, config, connection_manager):
        self.config = config
        self.connection = connection_manager
        
    def send_file(self, file_path):
        """Send a file to connected peer"""
        if not self.connection.is_connected():
            logger.error("Not connected")
            return False
        
        try:
            file_path = Path(file_path)
            file_size = file_path.stat().st_size
            
            # Calculate packet size based on file size
            packet_size = max(self.PACKET_SIZE, file_size // self.TOTAL_PACKETS)
            total_packets = (file_size + packet_size - 1) // packet_size
            
            # Send file metadata
            metadata = {
                'type': 'FILE_TRANSFER',
                'filename': file_path.name,
                'size': file_size,
                'packet_size': packet_size,
                'total_packets': total_packets,
                'checksum': self._calculate_checksum(file_path)
            }
            
            self._send_json(metadata)
            
            # Wait for acknowledgment
            ack = self._receive_json()
            if ack.get('status') != 'READY':
                logger.error("Peer not ready to receive")
                return False
            
            # Send file in packets
            progress = ProgressBar(total_packets, f"Uploading {file_path.name}")
            
            with open(file_path, 'rb') as f:
                packet_num = 0
                
                while packet_num < total_packets:
                    try:
                        # Read packet
                        data = f.read(packet_size)
                        if not data:
                            break
                        
                        # Send packet with header
                        packet = {
                            'packet_num': packet_num,
                            'data': data.hex()
                        }
                        self._send_json(packet)
                        
                        # Wait for acknowledgment
                        ack = self._receive_json()
                        if ack.get('status') != 'ACK':
                            raise Exception("Packet not acknowledged")
                        
                        packet_num += 1
                        progress.update(packet_num)
                        
                    except KeyboardInterrupt:
                        self._send_json({'type': 'CANCEL'})
                        logger.error("\n❌ Transfer cancelled by user")
                        return False
                    except Exception as e:
                        self._send_json({'type': 'ERROR', 'message': str(e)})
                        logger.error(f"\n❌ Interference in data transfer: {e}")
                        return False
            
            progress.finish()
            
            # Send completion signal
            self._send_json({'type': 'COMPLETE'})
            
            # Wait for final verification
            final = self._receive_json()
            if final.get('status') == 'SUCCESS':
                return True
            else:
                logger.error(f"Transfer verification failed: {final.get('message')}")
                return False
            
        except ConnectionError:
            logger.error("❌ Connection lost during transfer")
            return False
        except Exception as e:
            logger.error(f"❌ Send failed: {e}")
            return False
    
    def receive_file(self):
        """Receive a file from connected peer"""
        try:
            # Receive metadata
            metadata = self._receive_json()
            
            if metadata.get('type') != 'FILE_TRANSFER':
                return False
            
            filename = metadata['filename']
            file_size = metadata['size']
            packet_size = metadata['packet_size']
            total_packets = metadata['total_packets']
            expected_checksum = metadata['checksum']
            
            logger.info(f"\n📥 Incoming file: {filename} ({self._format_size(file_size)})")
            
            # Prepare output path
            output_path = Path(self.config.download_dir) / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Send ready signal
            self._send_json({'status': 'READY'})
            
            # Receive file packets
            progress = ProgressBar(total_packets, f"Downloading {filename}")
            
            with open(output_path, 'wb') as f:
                packet_num = 0
                
                while packet_num < total_packets:
                    try:
                        # Receive packet
                        packet = self._receive_json()
                        
                        if packet.get('type') == 'CANCEL':
                            logger.error("\n❌ Transfer cancelled by sender")
                            output_path.unlink()
                            return False
                        
                        if packet.get('type') == 'ERROR':
                            logger.error(f"\n❌ Transfer error: {packet.get('message')}")
                            output_path.unlink()
                            return False
                        
                        if packet.get('type') == 'COMPLETE':
                            break
                        
                        # Write packet data
                        data = bytes.fromhex(packet['data'])
                        f.write(data)
                        
                        # Send acknowledgment
                        self._send_json({'status': 'ACK'})
                        
                        packet_num += 1
                        progress.update(packet_num)
                        
                    except KeyboardInterrupt:
                        self._send_json({'type': 'CANCEL'})
                        logger.error("\n❌ Transfer cancelled by user")
                        output_path.unlink()
                        return False
                    except Exception as e:
                        logger.error(f"\n❌ Interference in data transfer: {e}")
                        output_path.unlink()
                        return False
            
            progress.finish()
            
            # Verify checksum
            actual_checksum = self._calculate_checksum(output_path)
            
            if actual_checksum == expected_checksum:
                self._send_json({'status': 'SUCCESS'})
                logger.info(f"✅ Saved to: {output_path}")
                return True
            else:
                self._send_json({'status': 'ERROR', 'message': 'Checksum mismatch'})
                logger.error("❌ File verification failed")
                output_path.unlink()
                return False
                
        except ConnectionError:
            logger.error("❌ Connection lost during transfer")
            return False
        except Exception as e:
            logger.error(f"❌ Receive failed: {e}")
            return False
    
    def _send_json(self, data):
        """Send JSON data"""
        message = json.dumps(data).encode()
        length = len(message).to_bytes(4, 'big')
        self.connection.socket.sendall(length + message)
    
    def _receive_json(self):
        """Receive JSON data"""
        length_bytes = self._receive_exact(4)
        length = int.from_bytes(length_bytes, 'big')
        message = self._receive_exact(length)
        return json.loads(message.decode())
    
    def _receive_exact(self, num_bytes):
        """Receive exact number of bytes"""
        data = b''
        while len(data) < num_bytes:
            chunk = self.connection.socket.recv(num_bytes - len(data))
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk
        return data
    
    def _calculate_checksum(self, file_path):
        """Calculate SHA256 checksum of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _format_size(self, size):
        """Format file size for display"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"