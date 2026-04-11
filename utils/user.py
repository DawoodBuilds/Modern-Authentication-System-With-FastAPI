from typing import Annotated
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import UserRepository
from core.security import create_access_token, create_refresh_token

async def create_user(user: Annotated[UserCreate, Form()], db: Annotated[AsyncSession, Depends(get_db)]):
    repo = UserRepository(db)
    result = await repo.create(user)
    return result
    
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):
    repo = UserRepository(db)
    user = await repo.authenticate(form_data.username, form_data.password)
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}