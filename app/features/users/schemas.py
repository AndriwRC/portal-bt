from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None
    role_id: Optional[int] = None


class UserUpdate(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None


class UserRead(UserBase):
    id: int
    role: Optional["RoleBase"] = None


class UserReadMin(UserBase):
    pass


class UserReadDetailed(UserRead):
    phone: Optional[str] = None
    role: Optional["RoleDetailed"] = None


class RoleBase(SQLModel):
    name: str


class RoleDetailed(RoleBase):
    permissions: list["PermissionBase"] = []


class PermissionBase(SQLModel):
    name: str
    label: str
    module: str
    description: Optional[str] = None
