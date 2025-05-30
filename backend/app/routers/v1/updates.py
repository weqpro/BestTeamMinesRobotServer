from fastapi import Depends
from fastapi.routing import APIRouter

from app.repository import UpdateRepository, get_update_repository
from app.schemas import UpdateSchema, UpdateCreateSchema

router = APIRouter(prefix="/update")


@router.get("/get", response_model=UpdateSchema | None)
async def get_update(
    update_repository: UpdateRepository = Depends(get_update_repository),
):
    return await update_repository.get_first_update()


@router.post("/create", response_model=UpdateSchema)
async def create_update(
    update_in: UpdateCreateSchema,
    update_repository: UpdateRepository = Depends(get_update_repository),
):
    update = await update_repository.create_update(data=update_in.data)
    return update
