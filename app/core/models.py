from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select
from typing import Type, TypeVar, Generic, Optional, List

ModelType = TypeVar("ModelType", bound=SQLModel)
ResponseType = TypeVar("ResponseType")


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


class APIResponse(BaseModel, Generic[ResponseType]):
    message: str
    data: Optional[ResponseType] = None
    errors: Optional[dict] = None
