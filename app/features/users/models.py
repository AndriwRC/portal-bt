from __future__ import annotations
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional

from ..visits.models import UserVisitLink

if TYPE_CHECKING:
    from ..auth.models import Role
    from ..hours.models import Hour
    from ..visits.models import Visit


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: str
    phone: str | None = None
    role_id: int | None = Field(default=None, foreign_key="roles.id")
    created_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    updated_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
    deleted_at: datetime | None = Field(default=None, nullable=True)

    role: Optional["Role"] = Relationship(back_populates="users")
    hours: list["Hour"] = Relationship(back_populates="user")
    scheduled_visits: list["Visit"] = Relationship(back_populates="responsible")
    attended_visits: list["Visit"] = Relationship(
        back_populates="assignees", link_model=UserVisitLink
    )
