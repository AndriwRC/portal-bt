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
    def __init__(self, db: Session):
        super().__init__(db, User)
