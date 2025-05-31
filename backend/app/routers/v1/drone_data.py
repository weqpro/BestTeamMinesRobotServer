from fastapi.routing import APIRouter

router = APIRouter(prefix="/drone_data")


@router.post("/detect_metal")
async def detect_metal():
    print("METAL DETECTED!")
    return {"status": "metal_detected"}
