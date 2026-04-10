from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True, pool_size=5, max_overflow=10)
AsyncLocalSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncLocalSession() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()