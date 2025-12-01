from sqlmodel import Session

from app.core.queries.base import (
    BaseQuery,
    CreateQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
)

from .models import User


class UserQueries(
    BaseQuery[User],
    CreateQueryMixin[User],
    UpdateQueryMixin[User],
    DeleteQueryMixin[User],
):
    model = User
