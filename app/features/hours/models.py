from datetime import date, time
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


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
    activity_type: Optional[int] = Field(
        default=None, foreign_key="parameter_values.id"
    )
