import bcrypt
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Any
from datetime import datetime, timedelta, timezone
from core.config import settings
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def create_access_token(data: dict[str, Any]):
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({"exp": expires, "type": "acesss"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm) 

def create_refresh_token(data: dict[str, Any]):
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expires_days)
    to_encode.update({"exp": expires, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm) 