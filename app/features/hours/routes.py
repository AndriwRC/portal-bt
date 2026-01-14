from typing import Annotated
from fastapi import APIRouter, Depends, Response

from app.core.dependencies.auth import AuthDep
from app.core.dependencies.db import SessionDep
from app.core.schemas.http import HTTPResponseModel

from .schemas import HourCreate, HourRead
from .services import HourService


def get_hours_service(db: SessionDep):
    return HourService(db)


ServiceDep = Annotated[HourService, Depends(get_hours_service)]

router = APIRouter(prefix="/hours", tags=["hours"])


@router.get("/", response_model=HTTPResponseModel[list[HourRead]])
def get_hours(response: Response, service: ServiceDep, user: AuthDep):
    result = service.get_hours(user.id)
    response.status_code = result.status_code

    return result


@router.post("/", response_model=HTTPResponseModel[HourRead])
def create_hour(
    hour: HourCreate, response: Response, service: ServiceDep, user: AuthDep
):
    result = service.create(data=hour, user_id=user.id)
    response.status_code = result.status_code

    return result
