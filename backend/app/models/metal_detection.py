import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, DateTime, Float

from .base import Base


class MetalDetection(Base):
    __tablename__ = "metal_detection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        server_default=func.now(),
    )

    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    robot_x: Mapped[float] = mapped_column(Float, nullable=False)
    robot_y: Mapped[float] = mapped_column(Float, nullable=False)
    robot_facing: Mapped[float] = mapped_column(Float, nullable=False)
