from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from .schemas import UserBase
from .permissions import PermissionEnum
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


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: PermissionEnum = Field(unique=True)
    label: str
    module: str
    description: Optional[str] = None

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    is_protected: bool = Field(default=False)

    permissions: list[Permission] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )
    users: list["User"] = Relationship(back_populates="role")


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=True)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    role: Optional[Role] = Relationship(back_populates="users")
    hours: list["Hour"] = Relationship(back_populates="user")
    scheduled_visits: list["Visit"] = Relationship(back_populates="responsible")
    attended_visits: list["Visit"] = Relationship(
        back_populates="assignees", link_model=UserVisitLink
    )
