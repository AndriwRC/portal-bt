from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Visit(SQLModel, table=True):
    __tablename__ = "visits"

    id: Optional[int] = Field(default=None, primary_key=True)
    equipment: str

    school_id: Optional[int] = Field(default=None, foreign_key="schools.id")
    responsible_id: Optional[int] = Field(default=None, foreign_key="users.id")
    hour_id: Optional[int] = Field(default=None, foreign_key="hours.id")


class UserVisitLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    visit_id: Optional[int] = Field(
        default=None, foreign_key="visits.id", primary_key=True
    )
