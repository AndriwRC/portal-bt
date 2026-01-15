from sqlmodel import select

from app.core.queries.base import(
    BaseQuery,
    CreateQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
)
from .models import School

class SchoolQueries(
    BaseQuery[School],
    CreateQueryMixin[School],
    UpdateQueryMixin[School],
    DeleteQueryMixin[School],
):
    model = School
    def get_by_email(self, email:str):
        statement = select(self.model).where(self.model.email == email)

        return self.db.exec(statement).first()

