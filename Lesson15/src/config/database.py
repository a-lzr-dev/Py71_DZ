# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from config.settings import settings
#
# engine = create_async_engine(settings.DATABASE_URL, echo=settings.DB_ECHO)
# AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
# # Dependency для FastAPI (если используется)
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine("mysql+mysqldb://root:password@localhost/general", echo=False)
engine = create_engine("sqlite:///db.sqlite_base")
session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)
session = session_maker()