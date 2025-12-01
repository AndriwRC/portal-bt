from pydantic import BaseModel
from typing import TypeVar, Generic

ResponseType = TypeVar("ResponseType")


class HTTPResponseModel(BaseModel, Generic[ResponseType]):
    status_code: int
    message: str
    data: ResponseType | None = None


def error_detail(msg: str, ctx: str | None = None):
    return [
        {
            "msg": msg,
            "ctx": {"error": ctx} if ctx else {},
        }
    ]
