import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
import sqlalchemy.exc

from app.utils import Singleton

from app.models import *
from app.models.base import Base


class RepositoryContext(metaclass=Singleton):
    def __init__(self) -> None:
        connection: str = "sqlite+aiosqlite:///:memory:"

        self.__engine: AsyncEngine = create_async_engine(
            connection,
            echo=True,
            connect_args={"check_same_thread": False},
            poolclass=None,
        )

        self.__session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.__engine, expire_on_commit=False
        )

    async def init_db(self):
        print("Connecting to db...", flush=True)
        try:
            async with self.__engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
        except sqlalchemy.exc.OperationalError:
            print("Failed (retry after 2s)", flush=True)
            await asyncio.sleep(2)
            await self.init_db()

    async def dispose(self) -> None:
        asyncio.run(self.__engine.dispose())

    @asynccontextmanager
    async def session_factory(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.__session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_repository_context() -> RepositoryContext:
    return RepositoryContext()
