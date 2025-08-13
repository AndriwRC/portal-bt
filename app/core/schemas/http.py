from typing import List
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

ResponseType = TypeVar("ResponseType")


class HTTPResponseModel(BaseModel, Generic[ResponseType]):
    status_code: int
    message: str
    data: Optional[ResponseType] = None
    errors: Optional[List] = None
