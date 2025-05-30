from fastapi import FastAPI
from sqlalchemy import create_engine

from app.models import *
from app.models import Base  # so Ruff won't curse


app = FastAPI()


def configure_app():
    engine = create_engine("sqlite:///data/db.db", echo=True)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    configure_app()
