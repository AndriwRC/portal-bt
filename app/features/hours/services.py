from fastapi import status

from app.core.schemas.http import HTTPResponseModel
from app.core.services.base import BaseService, CreateServiceMixin

from .models import Hour
from .queries import HourQueries
from .schemas import HourCreate


class HourService(BaseService[Hour, HourQueries], CreateServiceMixin[Hour]):
    model = Hour
    query_class = HourQueries

    def get_hours(self, user_id: int):
        data = self.queries.get_by_user(user_id)

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message="Hours retrieved successfully",
            data=data,
        )

    def create(self, data: HourCreate, user_id: int):
        data.user_id = user_id
        return super().create(data)
