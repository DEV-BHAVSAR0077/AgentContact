import base64
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from passlib.context import CryptContext
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from app.core.config import settings

# Argon2id context for passwords (requires passlib[argon2] and argon2-cffi)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# --- Envelope Encryption for API Keys ---

def _get_derived_key() -> bytes:
    """Derive a 256-bit key from the ENCRYPTION_MASTER_KEY string using HKDF"""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'agentflow-apikey-encryption',
    )
    return hkdf.derive(settings.ENCRYPTION_MASTER_KEY.encode('utf-8'))

def encrypt_api_key(plain_api_key: str) -> str:
    if not plain_api_key:
        return plain_api_key
    
    key = _get_derived_key()
    aesgcm = AESGCM(key)
    # Generate 12 byte (96 bit) nonce
    import os
    nonce = os.urandom(12)
    # Encrypt
    ciphertext = aesgcm.encrypt(nonce, plain_api_key.encode('utf-8'), None)
    # Return nonce + ciphertext as base64 string
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_api_key(encrypted_api_key_b64: str) -> str:
    if not encrypted_api_key_b64:
        return encrypted_api_key_b64
        
    try:
        encrypted_data = base64.b64decode(encrypted_api_key_b64.encode('utf-8'))
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        
        key = _get_derived_key()
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception:
        # If decryption fails, return a placeholder so the system doesn't crash, 
        # but the key will just be invalid.
        return ""
