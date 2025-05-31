from fastapi import Depends
from fastapi.routing import APIRouter

from app.repository import UpdateRepository, get_update_repository
from app.schemas import UpdateSchema, UpdateCreateSchema

router = APIRouter(prefix="/drone_data")


@router.post("/detect_metal")
async def detect_metal():
    print("METAL DETECTED!")
