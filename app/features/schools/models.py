from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..visits.models import Visit


class School(SQLModel, table=True):
    __tablename__ = "schools"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    address: str
    in_charge: str

    visits: list["Visit"] = Relationship(back_populates="school")
