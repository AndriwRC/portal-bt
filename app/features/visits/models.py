from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from ..users import User
from ..schools import School


class Visit(SQLModel, table=True):
    __tablename__ = "visits"

    id: Optional[int] = Field(default=None, primary_key=True)
    equipment: str

    school_id: Optional[int] = Field(default=None, foreign_key="schools.id")
    responsible_id: Optional[int] = Field(default=None, foreign_key="users.id")
    hour_id: Optional[int] = Field(default=None, foreign_key="hours.id")

    # Each visit have one responsable
    responsible: Optional["User"] = Relationship(back_populates="responsible_visits")
    # The visit is realice only on one school
    schools: Optional["School"] = Relationship(back_populates="schools")
    # Multiple user can realize a visit
    users: list["Visit"] = Relationship(
        back_populates="visits", link_model="UserVisitLink"
    )


class UserVisitLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    visit_id: Optional[int] = Field(
        default=None, foreign_key="visits.id", primary_key=True
    )
