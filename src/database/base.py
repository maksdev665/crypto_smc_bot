"""
Базовая конфигурация для работы с базой данных
"""

from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base

from src.config.settings import settings

Base = declarative_base()

class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self):
        self.engine: AsyncEngine = None
        self.async_session_maker: async_sessionmaker = None

    async def init(self):
        """Инициализация подключения к БД"""
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.LOG_LEVEL,
            poolcalss=NullPool
        )
        
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def create_tables(self):
        """Создание таблиц в БД"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self):
        """Удаление всех таблиц из БД"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Контекстный менеджер для сессии"""
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self):
        """Закрытие подключения к БД"""
        if self.engine:
            await self.engine.dispose()


# Создаем глобальный экземпляр менеджера БД
db_manager = DatabaseManager()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии БД"""
    async with db_manager.session() as session:
        yield session