import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, DateTime, String

from .base import Base


class Update(Base):
    __tablename__ = "update"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    data: Mapped[str] = mapped_column(String(30), nullable=False)
