from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    password: str
