from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from typing import Type, Generic, TypeVar

from ..constants import CRUDMessages
from ..queries.base import BaseQuery
from ..schemas.http import HTTPResponseModel, error_detail
from ..types import ModelType, CreateModelType

QueryType = TypeVar("QueryType", bound=BaseQuery)


class BaseService(Generic[ModelType, QueryType]):
    model: Type[ModelType]
    query_class: Type[QueryType]

    def __init__(self, db: Session):
        self.db = db
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

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_detail(msg=CRUDMessages.GET_NOT_FOUND),
            )

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message=CRUDMessages.GET_SUCCESS,
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_detail(
                    msg=CRUDMessages.CREATE_FAILED,
                    ctx=str(ex.args),
                ),
            )

        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            )
