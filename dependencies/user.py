from typing import Annotated
from fastapi import Depends, HTTPException
from core.security import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from jose import jwt, JWTError
from core.config import settings
from repositories.user import UserRepository

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="No token")
    except JWTError:
        raise HTTPException(status_code=401, detail="No token")
    
    repo = UserRepository(db)
    user = await repo.get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user