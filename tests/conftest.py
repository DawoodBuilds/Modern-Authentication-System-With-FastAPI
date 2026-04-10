import os
os.environ["TESTING"] = "1"
import pytest
from typing import AsyncGenerator, Any
from httpx import AsyncClient, ASGITransport
from main import app
from db.session import engine, get_db
from db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from core.config import settings

@pytest.fixture(scope="session")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
        
@pytest.fixture
async def db_session(test_db: Any) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.DATABASE_URL, echo=True, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    async with session_factory() as session:
        yield session
        await session.rollback()
    await engine.dispose()
        
@pytest.fixture
async def client(db_session: Any) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()