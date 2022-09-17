from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DatabaseConfig

async_engine = create_async_engine(DatabaseConfig.url)
AsyncSessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def init_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
