from pydantic import BaseModel


class UpdateSchema(BaseModel):
    data: str

    model_config = {"from_attributes": True}


class UpdateCreateSchema(BaseModel):
    data: str
