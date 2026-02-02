from sqlmodel import select
from datetime import datetime

from app.core.queries.base import (
    BaseQuery,
    CreateQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
)
from app.core.types import ModelType

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

    def get_by_ids(self, ids: list[int]):
        statement = select(self.model).where(self.model.id.in_(ids))
        return self.db.exec(statement).all()

    def delete(self, record: ModelType) -> ModelType:
        record.deleted_at = datetime.now()
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record
