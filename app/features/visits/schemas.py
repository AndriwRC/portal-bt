from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel
import datetime

from .models import VisitStatus
from features.schools.schemas import SchoolRead
from features.users.schemas import UserRead

class VisitBase(SQLModel):
    date:datetime.date
    time_start:datetime.time
    time_end:datetime.time


class VisitCreate(VisitBase):
    school_id:int

    status:VisitStatus = VisitStatus.SCHEDULED
    has_pc:bool = False
    has_videobeam:bool = False
    students_number:int
    observations:str | None = None


class VisitUpdate(SQLModel):
    date: datetime.date | None = None
    time_start: datetime.time | None = None
    time_end: datetime.time | None = None
    students_number:int | None = None
    observations:str | None = None

    assignee_ids: list[int] | None =  None


class VisitRead(VisitBase):
    id:int
    status: VisitStatus

    school:SchoolRead | None = None


class VisitReadMin(VisitBase):
    pass

class VisitReadDetailed(VisitRead):
    responsible_name:str
    has_pc:bool
    has_videobeam:bool
    observations:str
    students_number:int

    assignees: list[UserRead] = []
    responsible: UserRead | None = None




