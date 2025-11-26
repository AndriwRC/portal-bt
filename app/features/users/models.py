from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from .schemas import UserBase
from ..visits.models import UserVisitLink

if TYPE_CHECKING:
    from ..hours.models import Hour
    from ..visits.models import Visit


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permission_link"
    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permissions.id", primary_key=True
    )


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    roles: list[Role] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True
    )


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=True)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    roles: list[Role] = Relationship(link_model=UserRoleLink)
    hours: list["Hour"] = Relationship(back_populates="user")
    scheduled_visits: list["Visit"] = Relationship(back_populates="responsible")
    attended_visits: list["Visit"] = Relationship(
        back_populates="assignees", link_model=UserVisitLink
    )
