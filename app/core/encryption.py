import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings


def _get_encryption_key() -> bytes:
    """
    Retrieve and validate the encryption key from environment.
    Key must be exactly 32 bytes (256 bits) for AES-256-GCM.
    """
    key = settings.ENCRYPTION_KEY.encode('utf-8')
    if len(key) != 32:
        raise ValueError(
            f"ENCRYPTION_KEY must be exactly 32 bytes, got {len(key)} bytes. "
            "Generate a valid key using: python -c \"import os; print(os.urandom(32).hex())\""
        )
    return key


def encrypt(text: str) -> str:
    """
    Encrypt text using AES-256-GCM.
    
    Args:
        text: Plain text to encrypt
        
    Returns:
        Base64-encoded string containing nonce + ciphertext + tag
        
    Raises:
        ValueError: If encryption key is invalid
        Exception: If encryption fails
    """
    try:
        key = _get_encryption_key()
        aesgcm = AESGCM(key)
        
        # Generate a random 12-byte nonce (recommended for GCM)
        nonce = os.urandom(12)
        
        # Encrypt the text (encode to bytes first)
        ciphertext = aesgcm.encrypt(nonce, text.encode('utf-8'), None)
        
        # Combine nonce + ciphertext and encode as base64 for safe storage/transmission
        encrypted_data = base64.b64encode(nonce + ciphertext).decode('utf-8')
        
        return encrypted_data
        
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")


def decrypt(token: str) -> str:
    """
    Decrypt AES-256-GCM encrypted token.
    
    Args:
        token: Base64-encoded string containing nonce + ciphertext + tag
        
    Returns:
        Decrypted plain text
        
    Raises:
        ValueError: If encryption key is invalid or token is malformed
        Exception: If decryption fails (wrong key, corrupted data, etc.)
    """
    try:
        key = _get_encryption_key()
        aesgcm = AESGCM(key)
        
        # Decode from base64
        encrypted_data = base64.b64decode(token.encode('utf-8'))
        
        # Extract nonce (first 12 bytes) and ciphertext
        if len(encrypted_data) < 12:
            raise ValueError("Invalid encrypted data: too short")
        
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        
        # Decrypt and decode back to string
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode('utf-8')
        
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")
