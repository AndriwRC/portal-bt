from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

from .permissions import PermissionEnum

if TYPE_CHECKING:
    from ..users.models import User


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permission_link"
    role_id: int | None = Field(default=None, foreign_key="roles.id", primary_key=True)
    permission_id: int | None = Field(
        default=None, foreign_key="permissions.id", primary_key=True
    )


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: int | None = Field(default=None, primary_key=True)
    name: PermissionEnum = Field(unique=True)
    label: str
    module: str
    description: str | None = None

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    is_protected: bool = Field(default=False)

    permissions: list[Permission] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )
    users: list["User"] = Relationship(back_populates="role")
