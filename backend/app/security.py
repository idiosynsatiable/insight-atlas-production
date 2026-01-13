import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

def hash_password(pw: str) -> str:
    """Hash password using bcrypt. Automatically handles encoding and salting."""
    pw_bytes = pw.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

def verify_password(pw: str, pw_hash: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        pw_bytes = pw.encode('utf-8')
        hash_bytes = pw_hash.encode('utf-8')
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        return False

def create_access_token(subject: str, secret: str, expires_minutes: int = 60*24*7) -> str:
    exp = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": exp}
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_token(token: str, secret: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        return None
