from typing import Optional
from pydantic import EmailStr, SecretStr
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    phone: Optional[str]
    email: EmailStr
    password: str


class UserPublic(UserBase):
    id: int
    password: SecretStr
