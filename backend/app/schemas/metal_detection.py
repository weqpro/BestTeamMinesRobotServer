from pydantic import BaseModel


class MetalDetectionSchema(BaseModel):
    x: float
    y: float
    robot_x: float
    robot_y: float
    robot_facing: float
    timestamp: str

    model_config = {"from_attributes": True}


class MetalDetectionCreateSchema(BaseModel):
    x: float
    y: float
    robot_x: float
    robot_y: float
    robot_facing: float
