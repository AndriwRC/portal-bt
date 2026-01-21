from sqlmodel import select
from app.core.queries.base import BaseQuery, CreateQueryMixin

from .models import Hour


class HourQueries(
    BaseQuery[Hour],
    CreateQueryMixin[Hour],
):
    model = Hour

    def get_by_user(self, user_id: int):
        statement = select(self.model).where(self.model.user_id == user_id)

        return self.db.exec(statement).all()
