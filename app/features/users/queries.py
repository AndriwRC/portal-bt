from sqlmodel import select

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

    def get_by_email(self, email: str):
        statement = select(self.model).where(self.model.email == email)

        return self.db.exec(statement).first()
