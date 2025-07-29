from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class School(SQLModel, table=True):
    __tablename__ = "schools"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    address: str
    in_charge: str
