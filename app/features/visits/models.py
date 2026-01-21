from datetime import date, time, datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

if TYPE_CHECKING:
    from ..users.models import User
    from ..schools.models import School


class VisitStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class UserVisitLink(SQLModel, table=True):
    __tablename__ = "user_visit_link"
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    visit_id: int | None = Field(
        default=None, foreign_key="visits.id", primary_key=True
    )


class Visit(SQLModel, table=True):
    __tablename__ = "visits"

    id: int | None = Field(default=None, primary_key=True)

    date: date
    time_start: time
    time_end: time

    status: VisitStatus = Field(
        sa_column=Column(String, nullable=False, default=VisitStatus.SCHEDULED)
    )
    has_pc: bool = Field(default=False)
    has_videobeam: bool = Field(default=False)
    students_number: int
    observations: str | None = Field(default=None)

    created_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    updated_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    deleted_at: datetime | None = Field(default=None, nullable=True)

    school_id: int | None = Field(default=None, foreign_key="schools.id")
    responsible_id: int | None = Field(default=None, foreign_key="users.id")
    school: Optional["School"] = Relationship(back_populates="visits")
    responsible: Optional["User"] = Relationship(back_populates="scheduled_visits")
    assignees: list["User"] = Relationship(
        back_populates="attended_visits", link_model=UserVisitLink
    )
    # Register hours to this visit
    hours: list["Hour"] = Relationship(back_populates="visit")
