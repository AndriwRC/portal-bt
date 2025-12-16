from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel

class SchoolBase(SQLModel):
    name: str
    address: str
    email: EmailStr

class SchoolCreate(SchoolBase):
    in_charge: str
    phone: str

class SchoolUpdate(SQLModel):
    address: str | None = None
    in_charge: str | None = None
    phone: str | None = None
    email: EmailStr |None = None

class SchoolRead(SchoolBase):
    id: int

class SchoolReadMin(SchoolBase):
    pass

class SchoolReadDetailed(SchoolRead):
    in_charge: str | None = None
    phone: str | None = None
    asignt: str | None = None
