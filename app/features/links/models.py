from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field


class UserVisitLink(SQLModel, table=True):
    __tablename__ = "user_visit_link"
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    visit_id: Optional[int] = Field(
        default=None, foreign_key="visits.id", primary_key=True
    )
