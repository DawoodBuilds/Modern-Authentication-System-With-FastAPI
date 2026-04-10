from fastapi import FastAPI
from contextlib import asynccontextmanager
# from db.session import engine
# from db.base import Base
from routers.auth import router as auth_router

import os

@asynccontextmanager
async def lifespan(app: FastAPI):  
    if not os.getenv("TESTING"):
        import alembic.config
        import alembic.command
        alembic_conf = alembic.config.Config("alembic.ini")
        alembic.command.upgrade(alembic_conf, "head")
        print("✅ Database is connected") 
    yield
    print("🛑 Shutdown")
    
app = FastAPI(title="Authentication", version="0.2", lifespan=lifespan)
app.include_router(auth_router, prefix="/auth")