from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from core import settings


class DBHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self._engine = create_async_engine(
            url,
            echo=echo,
            pool_size=pool_size,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
        )
        self._async_session_maker: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def dispose(self) -> None:
        await self._engine.dispose()


db_helper = DBHelper(
    settings.db.database_url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
