from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Parameter(SQLModel, table=True):
    __tablename__ = "parameters"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    ref: str


class ParameterValue(SQLModel, table=True):
    __tablename__ = "parameter_values"

    id: Optional[int] = Field(default=None, primary_key=True)
    value: str
    parameter_id: Optional[int] = Field(default=None, foreign_key="parameters.id")
