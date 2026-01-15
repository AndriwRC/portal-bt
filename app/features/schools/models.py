from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime


if TYPE_CHECKING:
    from ..visits.models import Visit


class School(SQLModel, table=True):
    __tablename__ = "schools"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    address: str
    in_charge: str
    email: EmailStr = Field(unique=True)

    visits: list["Visit"] = Relationship(back_populates="school")
    created_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    updated_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    deleted_at: datetime | None = Field(default=None, nullable=True)
