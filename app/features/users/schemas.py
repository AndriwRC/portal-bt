from typing import Optional
from pydantic import EmailStr, SecretStr
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    phone: Optional[str] = None
    email: EmailStr
    password: str


class UserPublic(UserBase):
    id: int
    password: SecretStr


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None
