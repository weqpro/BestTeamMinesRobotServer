from fastapi.routing import APIRouter

router = APIRouter(prefix="/update")


@router.get("/get")
def get_update(): ...
