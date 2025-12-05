from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from app.features.auth.permissions import PermissionEnum
from app.features.users.models import User
from app.features.users.queries import UserQueries
from app.utils.jwt import decode_access_token

from ..dependencies.db import SessionDep
from ..schemas.http import error_detail

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    try:
        user_id = decode_access_token(token)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except InvalidTokenError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_detail(msg="Invalid token", ctx=str(ex)),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_queries = UserQueries(db)
    user = user_queries.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


AuthDep = Annotated[User, Depends(get_current_user)]


def check_permissions(*required_permissions: PermissionEnum):
    """Build a dependency to check if a user has the specified permissions"""

    def dependency(user: AuthDep):
        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned",
            )

        user_permissions = {permission.name for permission in user.role.permissions}

        for permission in required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this action",
                )

        return True

    return dependency
