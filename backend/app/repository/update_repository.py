from collections.abc import Callable
from typing import override
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.contracts import RepositoryBase
from app.models import Update
from app.repository import RepositoryContext, get_repository_context


class UpdateRepository(RepositoryBase[Update]):
    @override
    def __init__(self, context: RepositoryContext) -> None:
        _session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]] = (
            context.session_factory
        )
        super().__init__(_session_factory, Update)

    async def get_first_update(self) -> Update | None:
        async with self._session_maker() as session:
            stmt = (
                select(Update)
                .where(Update.is_processed == False)
                .order_by(Update.created_at)
                .limit(1)
                .with_for_update(skip_locked=True)
            )
            result = await session.execute(stmt)
            update = result.scalar_one_or_none()

            if update is not None:
                update.is_processed = True
                await session.commit()

            return update

    async def create_update(self, data: str) -> Update:
        async with self._session_maker() as session:
            update = Update(data=data)
            session.add(update)
            await session.commit()
            await session.refresh(update)
            return update


async def get_update_repository() -> UpdateRepository:
    context = get_repository_context()
    return UpdateRepository(context)
