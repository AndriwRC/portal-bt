from pydantic import BaseModel
from sqlmodel import SQLModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleBase(SQLModel):
    name: str


class RoleDetailed(RoleBase):
    permissions: list["PermissionBase"] = []


class PermissionBase(SQLModel):
    name: str
    label: str
    module: str
    description: str | None = None
