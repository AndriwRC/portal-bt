from sqlmodel import Session, select
from typing import Type, Generic
from datetime import datetime
from ..types import ModelType


class BaseQuery(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ModelType]:
        statement = select(self.model).where(self.model.deleted_at == None)
        return self.db.exec(statement).all()

    def get_by_id(self, id: int) -> ModelType | None:
        statement = select(self.model).where(self.model.id == id, self.model.deleted_at == None)
        return self.db.exec(statement).first()


class CreateQueryMixin(Generic[ModelType]):
    def create(self, data: ModelType) -> ModelType:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)

        return data


class UpdateQueryMixin(Generic[ModelType]):
    def update(self, record: ModelType, data: dict) -> ModelType:
        record.sqlmodel_update(data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record


class DeleteQueryMixin(Generic[ModelType]):
    def delete(self, record: ModelType) -> ModelType:
        self.db.delete(record)
        self.db.commit()

        return record
