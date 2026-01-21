from datetime import date, datetime, time
from pydantic import ConfigDict, computed_field
from sqlmodel import SQLModel

from .models import ActivityType, HourState


class HourBase(SQLModel):
    date: date
    time_in: time
    time_out: time
    activity_type: ActivityType
    state: HourState

    @computed_field
    @property
    def total(self) -> float:
        helper_date = date.today()
        dt_in = datetime.combine(helper_date, self.time_in)
        dt_out = datetime.combine(helper_date, self.time_out)
        time_delta = dt_out - dt_in

        return time_delta.total_seconds() / 3600


class HourCreate(HourBase):
    model_config = ConfigDict(extra="allow")

    evidence: str | None = None
    state: HourState | None = None


class HourRead(HourBase):
    id: int
    evidence: str | None = None
