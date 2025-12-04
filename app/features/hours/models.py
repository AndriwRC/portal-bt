from datetime import date, time
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..users.models import User


class HourState(str, Enum):
    PENDING = "pendiente"
    APPROVED = "aprobada"


class ActivityType(str, Enum):
    VISIT = "visita"
    ADMINISTRATIVE = "trabajo administrativo"
    MEETING = "reunión"


class Hour(SQLModel, table=True):
    __tablename__ = "hours"

    id: int | None = Field(default=None, primary_key=True)
    date: date
    time_in: time
    time_out: time
    evidence: str | None = Field(default=None, description="file path")
    activity_type: ActivityType | None = Field(default=ActivityType.VISIT)
    state: HourState | None = Field(default=HourState.PENDING)
    user_id: int | None = Field(default=None, foreign_key="users.id")

    user: Optional["User"] = Relationship(back_populates="hours")
