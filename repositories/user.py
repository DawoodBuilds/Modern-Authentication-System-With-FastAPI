from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User
# from typing import Any
from schemas.user import UserCreate
from fastapi import HTTPException
from sqlalchemy import select, or_
from core.security import get_password_hash, verify_password

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        
    async def create(self, user: UserCreate) -> User:
        user_exists = await self.get_user(user.username, user.email)
        if user_exists:
            raise HTTPException(status_code=404, detail="User already exists")
        hashed_password = get_password_hash(user.password.get_secret_value())
        data = User(first_name=user.first_name, last_name=user.last_name, username=user.username, email=user.email, hashed_password=hashed_password, address=user.address, phone=user.phone)
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)
        return data
        
    async def get_user(self, username: str | None = None, email: str | None = None) -> User | None:
        if username is None and email is None:
            raise HTTPException(status_code=400, detail="Both fields are empty")
        result = await self.db.execute(select(User).where(or_(User.username == username, User.email == email)))
        return result.scalar_one_or_none()
    
    async def user_exists_or_not(self, username: str | None = None, email: str | None = None) -> bool:
        result = await self.get_user(username, email)
        if result is None:
            return False
        return True
    
    async def authenticate(self, username: str, password: str):
        user = await self.get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        verified = verify_password(password, user.hashed_password)
        if not verified:
            raise HTTPException(status_code=404, detail="Wrong credentials")
        return user
        