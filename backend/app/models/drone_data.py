import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, DateTime, Float

from .base import Base


class Update(Base):
    __tablename__ = "update"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        server_default=func.now(),
    )

    ax: Mapped[int] = mapped_column(Integer, nullable=False)
    ay: Mapped[int] = mapped_column(Integer, nullable=False)
    az: Mapped[int] = mapped_column(Integer, nullable=False)
    distance: Mapped[float] = mapped_column(Float, nullable=False)
    metal_detect: Mapped[float] = mapped_column(Float, nullable=False)
