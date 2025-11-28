from pydantic import BaseModel
from typing import TypeVar, Generic

ResponseType = TypeVar("ResponseType")


class HTTPResponseModel(BaseModel, Generic[ResponseType]):
    status_code: int
    message: str
    data: ResponseType | None = None
    errors: list | None = None
