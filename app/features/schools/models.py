from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..visits import Visit


class School(SQLModel, table=True):
    __tablename__ = "schools"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    address: str
    in_charge: str

    # A school can be visited more than once
    visits: list["Visit"] = Relationship(back_populates="schools")
