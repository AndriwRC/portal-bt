from datetime import date, time
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..users.models import User
    from ..visits.models import Visit


class HourState(str, Enum):
    PENDING = "pendiente"
    APPROVED = "aprobada"


class ActivityType(str, Enum):
    VISIT = "visita"
    ADMINISTRATIVE = "trabajo administrativo"
    MEETING = "reunión"


class Hour(SQLModel, table=True):
    __tablename__ = "hours"

    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    time_in: time
    time_out: time
    evidence: Optional[str] = Field(default=None, description="file path")
    activity_type: ActivityType = Field(default=ActivityType.VISIT)
    state: HourState = Field(default=HourState.PENDING)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    visit_id: Optional[int] = Field(default=None, foreign_key="visits.id")

    user: Optional["User"] = Relationship(back_populates="hours")
    visit: Optional["Visit"] = Relationship(back_populates="hours")
