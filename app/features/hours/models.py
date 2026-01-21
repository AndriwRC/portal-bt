from __future__ import annotations
from datetime import date, time
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..users.models import User


class HourState(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"


class ActivityType(str, Enum):
    VISIT = "visit"
    ADMINISTRATIVE = "administrative"
    MEETING = "meeting"


class Hour(SQLModel, table=True):
    __tablename__ = "hours"

    id: int | None = Field(default=None, primary_key=True)
    date: date
    time_in: time
    time_out: time
    evidence: str | None = Field(default=None, description="file path")
    activity_type: ActivityType | None = Field(
        sa_column=Column(String, nullable=False, default=ActivityType.VISIT)
    )
    state: HourState | None = Field(
        sa_column=Column(String, nullable=False, default=HourState.PENDING)
    )
    user_id: int | None = Field(default=None, foreign_key="users.id")

    user: Optional["User"] = Relationship(back_populates="hours")
