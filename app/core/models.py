from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, select
from typing import Type, TypeVar, Generic, Optional, List

from .constants import CRUDMessages
from .schemas.http import HTTPResponseModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateModelType = TypeVar("CreateModelType", bound=SQLModel)
UpdateModelType = TypeVar("UpdateModelType", bound=SQLModel)


class BaseQuery(Generic[ModelType, CreateModelType, UpdateModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get_all(self) -> List[ModelType]:
        statement = select(self.model)
        return self.db.exec(statement).all()

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.get(self.model, id)

    def create(self, data: CreateModelType) -> ModelType:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)

        return data

    def update(self, record: ModelType, data: UpdateModelType) -> ModelType:
        record.sqlmodel_update(data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record

    def delete(self, record: ModelType) -> ModelType:
        self.db.delete(record)
        self.db.commit()

        return record


class BaseService(Generic[ModelType, CreateModelType, UpdateModelType]):
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

    def update(self, id: int, data: UpdateModelType):
        record = self.queries.get_by_id(id)

        if record:
            new_data = data.model_dump(exclude_unset=True)
            updated = self.queries.update(record, new_data)
            return HTTPResponseModel(
                status_code=status.HTTP_200_OK,
                message=CRUDMessages.UPDATE_SUCCESS,
                data=updated,
            )

        return HTTPResponseModel(
            status_code=status.HTTP_404_NOT_FOUND,
            message=CRUDMessages.UPDATE_FAILED,
            errors=[{"detail": CRUDMessages.GET_NOT_FOUND}],
        )

    def delete(self, id: int):
        record = self.queries.get_by_id(id)

        if record:
            deleted = self.queries.delete(record)

            return HTTPResponseModel(
                status_code=status.HTTP_200_OK,
                message=CRUDMessages.DELETE_SUCCESS,
                data=deleted,
            )

        return HTTPResponseModel(
            status_code=status.HTTP_404_NOT_FOUND,
            message=CRUDMessages.DELETE_FAILED,
            errors=[{"detail": CRUDMessages.GET_NOT_FOUND}],
        )
