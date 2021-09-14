from pydantic import BaseModel


class BaseRoleSchema(BaseModel):
    name: str
    default: bool
    permissions: int

    class Config:
        orm_mode = True


class CreateRoleSchema(BaseRoleSchema):
    pass


class RoleSchema(BaseRoleSchema):
    id: int
