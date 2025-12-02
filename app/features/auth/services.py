from fastapi import HTTPException, status
from sqlmodel import Session

from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token

from .schemas import Token
from ..users.models import User
from ..users.queries import UserQueries


class AuthService:
    model = User
    query_class = UserQueries

    def __init__(self, db: Session):
        self.queries = self.query_class(db)

    def login(self, email: str, password: str) -> Token:
        user = self.queries.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": str(user.id)})

        return Token(access_token=access_token)
