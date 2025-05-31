from collections.abc import Callable
from typing import override
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.contracts import RepositoryBase
from app.models import MetalDetection
from app.repository import RepositoryContext, get_repository_context


class MetalDetectionRepository(RepositoryBase[MetalDetection]):
    @override
    def __init__(self, context: RepositoryContext) -> None:
        _session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]] = (
            context.session_factory
        )
        super().__init__(_session_factory, MetalDetection)

    async def create_detection(
        self, x: float, y: float, robot_x: float, robot_y: float, robot_facing: float
    ) -> MetalDetection:
        async with self._session_maker() as session:
            detection = MetalDetection(
                x=x, y=y, robot_x=robot_x, robot_y=robot_y, robot_facing=robot_facing
            )
            session.add(detection)
            await session.commit()
            await session.refresh(detection)
            return detection

    async def get_all_detections(self) -> list[MetalDetection]:
        async with self._session_maker() as session:
            stmt = select(MetalDetection).order_by(MetalDetection.created_at.desc())
            result = await session.execute(stmt)
            return list(result.scalars().all())


async def get_metal_detection_repository() -> MetalDetectionRepository:
    context = get_repository_context()
    return MetalDetectionRepository(context)
