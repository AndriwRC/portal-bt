from fastapi import APIRouter, Depends, Response
from typing import Annotated

from app.core.dependencies.auth import check_permissions
from app.core.dependencies.db import SessionDep
from app.core.schemas.http import HTTPResponseModel
from app.features.auth.permissions import PermissionEnum
from app.core.dependencies.auth import AuthDep

from .schemas import (
    SchoolCreate,
    SchoolRead,
    SchoolReadDetailed,
    SchoolReadMin,
    SchoolUpdate,
)
from .services import SchoolService


def get_school_service(db: SessionDep):
    return SchoolService(db)


ServiceDep = Annotated[SchoolService, Depends(get_school_service)]

router = APIRouter(prefix="/schools", tags=["schools"])


@router.get("/", response_model=HTTPResponseModel[list[SchoolRead]])
def get_schools(response: Response, service: ServiceDep):
    result = service.get_all()
    response.status_code = result.status_code

    return result


@router.get("/{school_id}", response_model=HTTPResponseModel[SchoolReadDetailed])
def get_school(school_id: int, response: Response, service: ServiceDep):
    result = service.get_by_id(school_id)
    response.status_code = result.status_code

    return result


@router.post("/", response_model=HTTPResponseModel[SchoolReadDetailed])
def create_school(
    school: SchoolCreate, response: Response, service: ServiceDep, current_user: AuthDep
):
    result = service.create(school)
    response.status_code = result.status_code

    return result


@router.patch("/{school_id}", response_model=HTTPResponseModel[SchoolReadDetailed])
def update_school(
    school_id: int,
    data: SchoolUpdate,
    response: Response,
    service: ServiceDep,
    current_user: AuthDep,
):
    result = service.update(school_id, data)
    response.status_code = result.status_code

    return result


@router.delete(
    "/{school_id}",
    response_model=HTTPResponseModel[SchoolReadMin],
    dependencies=[Depends(check_permissions(PermissionEnum.SCHOOL_MANAGE))],
)
def delete_school(school_id: int, response: Response, service: ServiceDep):
    result = service.delete(school_id)
    response.status_code = result.status_code

    return result
