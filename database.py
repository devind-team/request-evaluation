"""Открытие соединения с базой данных."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel # noqa

from settings import get_settings # noqa

engine = create_async_engine(
    get_settings().db_sync_connections, echo=True, future=True
)


async def init_db() -> None:
    """Функция инициализации базы данных."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Функция получения сессии."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
