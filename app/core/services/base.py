from fastapi import status
from sqlalchemy.exc import IntegrityError
from typing import Type, Generic

from ..constants import CRUDMessages
from ..queries.base import BaseQuery
from ..schemas.http import HTTPResponseModel
from ..types import ModelType, CreateModelType


class BaseService(Generic[ModelType]):
    def __init__(self, queries: BaseQuery, model: Type[ModelType]):
        self.queries = queries
        self.model = model

    def get_all(self) -> HTTPResponseModel:
        data = self.queries.get_all()

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message=CRUDMessages.LIST_SUCCESS if data else CRUDMessages.LIST_EMPTY,
            data=data,
        )

    def get_by_id(self, id: int) -> HTTPResponseModel:
        data = self.queries.get_by_id(id)

        if data:
            return HTTPResponseModel(
                status_code=status.HTTP_200_OK,
                message=CRUDMessages.GET_SUCCESS,
                data=data,
            )

        return HTTPResponseModel(
            status_code=status.HTTP_404_NOT_FOUND,
            message=CRUDMessages.GET_NOT_FOUND,
            data=data,
        )


class CreateServiceMixin(Generic[CreateModelType]):
    def create(self, data: CreateModelType) -> HTTPResponseModel:
        try:
            validated = self.model.model_validate(data)
            result = self.queries.create(validated)

            return HTTPResponseModel(
                status_code=status.HTTP_201_CREATED,
                message=CRUDMessages.CREATE_SUCCESS,
                data=result,
            )

        except IntegrityError as ex:
            return HTTPResponseModel(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CRUDMessages.CREATE_FAILED,
                errors=[{"detail": str(ex.orig)}],
            )
