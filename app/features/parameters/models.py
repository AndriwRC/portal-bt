from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from ..hours import Hour


class Parameter(SQLModel, table=True):
    __tablename__ = "parameters"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    ref: str

    # I dude on this
    parameterValues: list["ParameterValue"] = Relationship(back_populates="parameter")


class ParameterValue(SQLModel, table=True):
    __tablename__ = "parameter_values"

    id: Optional[int] = Field(default=None, primary_key=True)
    value: str
    parameter_id: Optional[int] = Field(default=None, foreign_key="parameters.id")

    #
    parameter: Optional["Parameter"] = Relationship(back_populates="parameterValues")
    # Multuple hours can have the same parameter value
    hours: list["Hour"] = Relationship(back_populates="activity_type")
