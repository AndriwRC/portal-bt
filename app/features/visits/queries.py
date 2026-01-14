from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from sqlalchemy import and_
from datetime import time, date


from app.core.queries.base import (
    BaseQuery,
    CreateQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
)

from .models import Visit, VisitStatus
from app.features.schools.models import School


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
            selectinload(self.model.assignees),
        )

    def check_overlap(
        self, school_id: int, visit_date: date, start: time, end: time, exclude_visit_id: int | None = None
    ) -> bool:
        statement = select(self.model).where(
            self.model.school_id == school_id,
            self.model.date == visit_date,
            self.model.status != VisitStatus.CANCELLED,
            and_(
                self.model.time_start < end,
                self.model.time_end > start,
            ),
        )
        if exclude_visit_id:
            statement = statement.where(self.model.id != exclude_visit_id)

        result = self.db.exec(statement).first()
        return result is not None
