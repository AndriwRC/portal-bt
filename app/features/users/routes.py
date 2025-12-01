from fastapi import APIRouter, Depends, Response
from typing import Annotated

from app.core.schemas.http import HTTPResponseModel
from app.database.core import SessionDep

from .schemas import UserCreate, UserRead, UserReadDetailed, UserReadMin, UserUpdate
from .services import UserService


def get_user_service(db: SessionDep):
    return UserService(db)


ServiceDep = Annotated[UserService, Depends(get_user_service)]

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=HTTPResponseModel[list[UserRead]])
def get_users(response: Response, service: ServiceDep):
    result = service.get_all()
    response.status_code = result.status_code

    return result


@router.get("/{user_id}", response_model=HTTPResponseModel[UserReadDetailed])
def get_user(user_id: int, response: Response, service: ServiceDep):
    result = service.get_by_id(user_id)
    response.status_code = result.status_code

    return result


@router.post("/", response_model=HTTPResponseModel[UserReadDetailed])
def create_user(user: UserCreate, response: Response, service: ServiceDep):
    result = service.create(user)
    response.status_code = result.status_code

    return result


@router.patch("/{user_id}", response_model=HTTPResponseModel[UserReadDetailed])
def update_user(
    user_id: int, data: UserUpdate, response: Response, service: ServiceDep
):
    result = service.update(user_id, data)
    response.status_code = result.status_code

    return result


@router.delete("/{user_id}", response_model=HTTPResponseModel[UserReadMin])
def delete_user(user_id: int, response: Response, service: ServiceDep):
    result = service.delete(user_id)
    response.status_code = result.status_code

    return result
