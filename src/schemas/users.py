from uuid import UUID

from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True


class UserSchema(BaseUserSchema):
    id: UUID


class UserCreateSchema(BaseUserSchema):
    pass
