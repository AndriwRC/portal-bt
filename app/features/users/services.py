from fastapi import HTTPException, status

from app.core.constants import CRUDMessages
from app.core.services.base import BaseService, CreateServiceMixin
from app.core.schemas.http import HTTPResponseModel, error_detail

from .models import User
from .queries import UserQueries
from .schemas import UserCreate, UserUpdate


class UserService(BaseService[User, UserQueries], CreateServiceMixin[UserCreate]):
    model = User
    query_class = UserQueries

    def update(self, id: int, data: UserUpdate):
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
        updated = self.queries.update(record, new_data)

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
