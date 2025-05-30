from collections.abc import Callable
from typing import override
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

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


async def get_update_repository() -> UpdateRepository:
    context = get_repository_context()
    return UpdateRepository(context)
