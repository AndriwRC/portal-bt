from fastapi import status
from sqlmodel import Session, SQLModel, select
from typing import Type, TypeVar, Generic, Optional, List

from .constants import CRUDMessages
from .schemas.http import HTTPResponseModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseQuery(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get_all(self) -> List[ModelType]:
        statement = select(self.model)
        return self.db.exec(statement).all()

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.get(self.model, id)


class BaseService:
    def __init__(self, queries: BaseQuery):
        self.queries = queries

    def get_all(self) -> HTTPResponseModel:
        # Business logic, permissions, exceptions
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
