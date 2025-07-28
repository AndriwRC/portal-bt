from typing import List
from fastapi import APIRouter, Depends, Response

from app.core.models import APIResponse
from app.database.core import get_session

from .queries import UserQueries
from .services import UserService


def get_user_queries(db=Depends(get_session)):
    return UserQueries(db)


def get_user_service(queries=Depends(get_user_queries)):
    return UserService(queries)


router = APIRouter(prefix="/users")


@router.get("/", response_model=APIResponse[List])
def get_users(response: Response, service: UserService = Depends(get_user_service)):
    return service.get_all(response)
