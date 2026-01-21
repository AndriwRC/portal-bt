from pydantic import EmailStr
from sqlmodel import SQLModel
from typing import Optional

from ..auth.schemas import RoleBase, RoleDetailed


class UserBase(SQLModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    phone: str | None = None
    role_id: int | None = None


class UserUpdate(SQLModel):
    name: str | None = None
    phone: str | None = None
    role_id: int | None = None


class UserRead(UserBase):
    id: int
    role: Optional["RoleBase"] = None


class UserReadMin(UserBase):
    pass


class UserReadDetailed(UserRead):
    phone: str | None = None
    role: Optional["RoleDetailed"] = None
