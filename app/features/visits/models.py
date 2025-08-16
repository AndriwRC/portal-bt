from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..users.models import User
    from ..schools.models import School
    from ..hours.models import Hour


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

    school_id: Optional[int] = Field(default=None, foreign_key="schools.id")
    responsible_id: Optional[int] = Field(default=None, foreign_key="users.id")
    # hour_id: Optional[int] = Field(default=None, foreign_key="hours.id")

    # Each visit have one responsable
    responsible: Optional["User"] = Relationship(back_populates="responsible_visits")
    # The visit is realice only on one school
    schools: Optional["School"] = Relationship(back_populates="visits")
    # Multiple user can realize a visit
    users: list["User"] = Relationship(
        back_populates="visits", link_model=UserVisitLink
    )
    # Register hours to this visit
    hours: list["Hour"] = Relationship(back_populates="visit")
