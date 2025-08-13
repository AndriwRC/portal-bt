from __future__ import annotations
from datetime import date, time
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..users import User
    from ..parameters import ParameterValue
    from ..visits import Visit


class Hour(SQLModel, table=True):
    __tablename__ = "hours"

    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    time_in: time
    time_out: time
    evidence: Optional[str] = Field(default=None, description="Ruta del archivo")
    state: Optional[str] = Field(default="Pendiente")

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    visit_id: Optional[int] = Field(default=None, foreign_key="visits.id")
    activity_type_id: Optional[int] = Field(
        default=None, foreign_key="parameter_values.id"
    )

    # An hour is register by one user
    user: Optional["User"] = Relationship(back_populates="hours")

    visit: Optional["Visit"] = Relationship(back_populates="hours")

    # Only one activity is register on an hour
    activity_type: Optional["ParameterValue"] = Relationship(back_populates="hours")
