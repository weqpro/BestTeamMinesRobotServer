from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.repository import RepositoryContext, get_repository_context
from app.routers.v1 import updates_router, drone_data_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    context: RepositoryContext = get_repository_context()
    await context.init_db()
    print("Connected to database", flush=True)

    yield

    await context.dispose()
    print("Closed the connection to database", flush=True)


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(updates_router)
app.include_router(drone_data_router)
