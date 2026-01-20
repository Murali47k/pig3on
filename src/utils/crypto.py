"""
Cryptography helper for Pig3on
Simple encryption wrapper for future encryption support
"""

import hashlib

class CryptoHelper:
    """Helper class for encryption operations"""
    
    def __init__(self):
        pass
    
    def hash_data(self, data):
        """Hash data using SHA256"""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()
    
    def encrypt(self, data):
        """Encrypt data (placeholder for future implementation)"""
        # For now, return data as-is
        # In future, can add AES encryption
        return data
    
    def decrypt(self, data):
        """Decrypt data (placeholder for future implementation)"""
        # For now, return data as-is
        # In future, can add AES decryption
        return data