from pydantic import BaseModel


class DroneData(BaseModel):
    ax: int
    ay: int
    az: int
    distance: float
    metal_detect: float
