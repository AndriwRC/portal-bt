from datetime import date, time
from pydantic import ConfigDict
from sqlmodel import SQLModel

from .models import ActivityType, HourState


class HourBase(SQLModel):
    date: date
    time_in: time
    time_out: time
    activity_type: ActivityType
    state: HourState


class HourCreate(HourBase):
    model_config = ConfigDict(extra="allow")

    evidence: str | None = None
    state: HourState | None = None


class HourRead(HourBase):
    id: int
    evidence: str | None = None
