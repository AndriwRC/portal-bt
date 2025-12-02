from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.core.dependencies.db import SessionDep

from .schemas import Token
from .services import AuthService

def get_auth_service(db: SessionDep):
    return AuthService(db)

ServiceDep = Annotated[AuthService, Depends(get_auth_service)]

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: ServiceDep):
    return service.login(form_data.username, form_data.password)
