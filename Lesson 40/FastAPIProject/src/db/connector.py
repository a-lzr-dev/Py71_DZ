import asyncio
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker as create_async_session_maker

from ..settings import settings

async_engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = create_async_session_maker(bind=async_engine, autocommit=False, autoflush=False)

async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

async def check_database(session: AsyncSession) -> bool:
    try:
        await asyncio.wait_for(session.execute(text("SELECT 1")), timeout=5.0)
        return True
    except (asyncio.TimeoutError, SQLAlchemyError):
        return False