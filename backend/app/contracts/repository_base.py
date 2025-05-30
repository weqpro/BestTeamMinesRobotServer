from contextlib import AbstractAsyncContextManager
from typing import Type
from collections.abc import Callable, Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import ColumnExpressionArgument


class RepositoryBase[T]:
    def __init__(
        self,
        session_maker: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        model: Type[T],
    ):
        self._session_maker = session_maker
        self._model = model

    async def create(self, value: T) -> T:
        """Adds new object to database"""
        async with self._session_maker() as session:
            session.add(value)
            await session.commit()
            await session.refresh(value)
            return value

    async def delete(self, value: T) -> None:
        async with self._session_maker() as session:
            await session.delete(value)
            await session.commit()
            return

    async def find(
        self,
        *order_by: ColumnElement | str,
    ) -> Sequence[T]:
        async with self._session_maker() as session:
            stmt = select(self._model).order_by(*order_by)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def find_by_condition(
        self,
        condition: ColumnExpressionArgument[bool],
        *order_by: ColumnElement | str,
    ) -> Sequence[T]:
        async with self._session_maker() as session:
            stmt = select(self._model).where(condition).order_by(*order_by)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update(self, condition: ColumnExpressionArgument[bool], **values) -> None:
        async with self._session_maker() as session:
            stmt = update(self._model).where(condition).values(**values)
            await session.execute(stmt)
            await session.commit()
            return
