from fastapi import status
from app.core.constants import CRUDMessages
from app.core.models import BaseService
from app.core.schemas.http import HTTPResponseModel
from .queries import UserQueries


class UserService(BaseService):
    queries = UserQueries

