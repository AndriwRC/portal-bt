from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from typing import Type, Generic, TypeVar


from ..constants import CRUDMessages
from ..queries.base import BaseQuery
from ..schemas.http import HTTPResponseModel
from ..types import ModelType, CreateModelType

QueryType = TypeVar("QueryType", bound=BaseQuery)

class BaseService(Generic[ModelType, QueryType]):
    model: Type[ModelType]
    query_class: Type[QueryType]

    def __init__(self, db: Session):
        self.queries = self.query_class(db)

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
