from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class ParameterType(str, Enum):
    TEXT = "text"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DECIMAL = "decimal"
    JSON = "json"
    SELECT = "select"


class Parameter(SQLModel, table=True):
    __tablename__ = "parameters"

    id: int | None = Field(default=None, primary_key=True)

    # Unique internal reference
    key: str = Field(index=True, unique=True)

    # Human-readable reference
    name: str
    description: str

    type: ParameterType = Field(default=ParameterType.TEXT)
    editable: bool = Field(default=True)
    default_value: str | None = None
    values: list["ParameterValue"] = Relationship(back_populates="parameter")

    # I dude on this
    parameterValues: list["ParameterValue"] = Relationship(back_populates="parameter")


class ParameterValue(SQLModel, table=True):
    __tablename__ = "parameter_values"

    id: int | None = Field(default=None, primary_key=True)
    value: str
    parameter_id: int | None = Field(
        default=None, foreign_key="parameters.id", index=True
    )

    parameter: Optional["Parameter"] = Relationship(back_populates="values")
