import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

from app.core.config import get_settings

setting = get_settings()

SECRET_KEY = setting.secret_key

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Check your .env file.")

ALGORITHM = "HS256"
EXPIRE_MINUTES = int(setting.access_token_expire_minutes)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])