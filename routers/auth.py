from fastapi import APIRouter, Depends, Header, HTTPException
from utils.user import create_user, login_user
from typing import Annotated
from core.security import Token, create_access_token, create_refresh_token
from typing import Any
from db.models.user import User
from dependencies.user import get_current_user
from core.rate_limit import limiter
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from jose import jwt, JWTError
from core.config import settings

router = APIRouter(tags=["Auth"])

@router.post("/register", description="Register User", status_code=201)
@limiter.limit("5/minute")  # type: ignore
async def register(user: Annotated[User, Depends(create_user)]):
    return user

@router.post("/login", description="Login", response_model=Token)
@limiter.limit("5/minute") # type: ignore
async def login(token: Annotated[dict[str, Any], Depends(login_user)]):
    return token

@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post("/refresh")
async def refresh_token(
    refresh_token: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(401)
        username = payload.get("sub")
        new_access = create_access_token({"sub": username})
        new_refresh = create_refresh_token({"sub": username})
        return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(401, "Invalid refresh Token")