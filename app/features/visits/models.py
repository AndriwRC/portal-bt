from datetime import date, time
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..users.models import User
    from ..schools.models import School


class UserVisitLink(SQLModel, table=True):
    __tablename__ = "user_visit_link"
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    visit_id: Optional[int] = Field(
        default=None, foreign_key="visits.id", primary_key=True
    )


class Visit(SQLModel, table=True):
    __tablename__ = "visits"

    id: Optional[int] = Field(default=None, primary_key=True)
    equipment: str
    date: date
    time_start: time
    time_end: time

    school_id: Optional[int] = Field(default=None, foreign_key="schools.id")
    responsible_id: Optional[int] = Field(default=None, foreign_key="users.id")

    school: Optional["School"] = Relationship(back_populates="visits")
    responsible: Optional["User"] = Relationship(back_populates="scheduled_visits")
    assignees: list["User"] = Relationship(
        back_populates="attended_visits", link_model=UserVisitLink
    )
