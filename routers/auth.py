from fastapi import APIRouter, Depends
from utils.user import create_user, login_user
from typing import Annotated
from core.security import Token
from typing import Any
from db.models.user import User
from dependencies.user import get_current_user

router = APIRouter(tags=["Auth"])

@router.post("/register", description="Register User", status_code=201)
async def register(user: Annotated[User, Depends(create_user)]):
    return user

@router.post("/login", description="Login", response_model=Token)
async def login(token: Annotated[dict[str, Any], Depends(login_user)]):
    return token

@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
