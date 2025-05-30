from pydantic import BaseModel
from datetime import datetime


class UpdateSchema(BaseModel):
    id: int
    created_at: datetime
    is_processed: bool
    data: str

    model_config = {"from_attributes": True}


class UpdateCreateSchema(BaseModel):
    data: str
