from typing import List
from fastapi import APIRouter, Depends, Response

from app.core.schemas.http import HTTPResponseModel
from app.database.core import get_session

from .schemas import UserCreate, UserPublic, UserUpdate
from .queries import UserQueries
from .services import UserService


def get_user_queries(db=Depends(get_session)):
    return UserQueries(db)


def get_user_service(queries=Depends(get_user_queries)):
    return UserService(queries)


router = APIRouter(prefix="/users")


@router.get("/", response_model=HTTPResponseModel[List[UserPublic]])
def get_users(response: Response, service: UserService = Depends(get_user_service)):
    result = service.get_all()
    response.status_code = result.status_code

    return result


@router.get("/{user_id}", response_model=HTTPResponseModel[UserPublic])
def get_user(
    user_id: int, response: Response, service: UserService = Depends(get_user_service)
):
    result = service.get_by_id(user_id)
    response.status_code = result.status_code

    return result


@router.post("/", response_model=HTTPResponseModel[UserPublic])
def create_user(
    user: UserCreate,
    response: Response,
    service: UserService = Depends(get_user_service),
):
    result = service.create(user)
    response.status_code = result.status_code

    return result


@router.patch("/{user_id}", response_model=HTTPResponseModel[UserPublic])
def update_user(
    user_id: int,
    data: UserUpdate,
    response: Response,
    service: UserService = Depends(get_user_service),
):
    result = service.update(user_id, data)
    response.status_code = result.status_code

    return result


@router.delete("/{user_id}", response_model=HTTPResponseModel[UserPublic])
def delete_user(
    user_id: int, response: Response, service: UserService = Depends(get_user_service)
):
    result = service.delete(user_id)
    response.status_code = result.status_code

    return result
