from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

from app.core.queries.base import(
    BaseQuery,
    CreateQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
)

from .models import Visit


class VisitQueries(
    BaseQuery[Visit],
    CreateQueryMixin[Visit],
    UpdateQueryMixin[Visit],
    DeleteQueryMixin[Visit],
):
    model = Visit

    def _base_query(self):
        return select(self.model).options(
            joinedload(self.model.school),
            joinedload(self.model.responsible),
            selectinload(self.model.assignees)
        )
