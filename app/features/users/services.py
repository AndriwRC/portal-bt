from fastapi import status

from app.core.constants import CRUDMessages
from app.core.models import BaseService
from app.core.schemas.http import HTTPResponseModel

from .models import User
from .queries import UserQueries
from .schemas import UserCreate, UserUpdate


class UserService(BaseService[User, UserCreate, UserUpdate]):
    queries = UserQueries

    def __init__(self, queries):
        super().__init__(queries, User)





