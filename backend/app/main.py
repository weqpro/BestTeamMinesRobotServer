from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import create_engine

from app.repository import RepositoryContext, get_repository_context
from app.routers.v1 import updates_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    context: RepositoryContext = get_repository_context()
    await context.init_db()
    print("Connected to database", flush=True)

    yield

    await context.dispose()
    print("Closed the connection to database", flush=True)


app = FastAPI(lifespan=lifespan)

app.include_router(updates_router)
