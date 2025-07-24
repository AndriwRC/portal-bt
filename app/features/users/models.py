from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class RolePermissionLink(SQLModel, table=True):
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
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str]
    email: str
    password: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    roles: list[Role] = Relationship(link_model=UserRoleLink)
