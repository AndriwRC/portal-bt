from fastapi import APIRouter, Depends, Response
from typing import Annotated

from app.core.dependencies.db import SessionDep
from app.core.dependencies.auth import AuthDep
from app.core.schemas.http import HTTPResponseModel

from .schemas import (
    VisitCreate,
    VisitRead,
    VisitReadDetailed,
    VisitReadMin,
    VisitUpdate,
)
from .services import VisitService


def get_visit_service(db: SessionDep):
    return VisitService(db)


ServiceDep = Annotated[VisitService, Depends(get_visit_service)]

router = APIRouter(prefix="/visits", tags=["visits"])


@router.get("/", response_model=HTTPResponseModel[list[VisitRead]])
def get_visits(response: Response, service: ServiceDep):
    result = service.get_all()
    response.status_code = result.status_code
    return result


@router.get("/{visit_id}", response_model=HTTPResponseModel[VisitReadDetailed])
def get_visit(visit_id: int, response: Response, service: ServiceDep):
    result = service.get_by_id(visit_id)
    response.status_code = result.status_code

    return result


@router.post("/", response_model=HTTPResponseModel[VisitReadDetailed])
def create_visit(
    visit: VisitCreate, response: Response, service: ServiceDep, current_user: AuthDep
):
    result = service.create(visit, user_obj=current_user)
    response.status_code = result.status_code

    return result


@router.patch("/{visit_id}", response_model=HTTPResponseModel[VisitReadDetailed])
def update_visit(
    visit_id: int, data: VisitUpdate, response: Response, service: ServiceDep
):
    result = service.update(visit_id, data)
    response.status_code = result.status_code

    return result


@router.delete("/{visit_id}", response_model=HTTPResponseModel[VisitRead])
def delete_visit(visit_id: int, response: Response, service: ServiceDep):
    result = service.delete(visit_id)
    response.status_code = result.status_code

    return result
