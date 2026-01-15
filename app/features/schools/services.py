from fastapi import HTTPException, status

from app.core.constants import CRUDMessages
from app.core.services.base import BaseService, CreateServiceMixin
from app.core.schemas.http import HTTPResponseModel, error_detail

from .models import School
from .queries import SchoolQueries
from .schemas import SchoolCreate, SchoolUpdate
from sqlalchemy.exc import IntegrityError


class SchoolService(
    BaseService[School, SchoolQueries], CreateServiceMixin[SchoolCreate]
):
    model = School
    query_class = SchoolQueries

    def update(self, id: int, data: SchoolUpdate):
        record = self.queries.get_by_id(id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_detail(
                    msg=CRUDMessages.UPDATE_FAILED,
                    ctx=CRUDMessages.GET_NOT_FOUND,
                ),
            )

        new_data = data.model_dump(exclude_unset=True)
        try:
            updated = self.queries.update(record, new_data)

        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_detail(
                    msg=CRUDMessages.UPDATE_FAILED,
                    ctx=CRUDMessages.CONFLICT_EMAIL,
                ),
            )

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message=CRUDMessages.UPDATE_SUCCESS,
            data=updated,
        )

    def delete(self, id: int):
        record = self.queries.get_by_id(id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_detail(
                    msg=CRUDMessages.DELETE_FAILED,
                    ctx=CRUDMessages.GET_NOT_FOUND,
                ),
            )

        deleted = self.queries.delete(record)

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message=CRUDMessages.DELETE_SUCCESS,
            data=deleted,
        )
