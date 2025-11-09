from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import db_settings

engine = create_async_engine(
    url=db_settings.DATABASE_URL_asyncpg,
    echo=False,
)


async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session