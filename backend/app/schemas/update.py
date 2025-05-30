from pydantic import BaseModel
from datetime import datetime


class UpdateSchema(BaseModel):
    created_at: datetime
    data: str

    model_config = {"from_attributes": True}


class UpdateCreateSchema(BaseModel):
    data: str
