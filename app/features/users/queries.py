from sqlmodel import Session

from app.core.models import BaseQuery

from .models import User
from .schemas import UserCreate, UserUpdate


class UserQueries(BaseQuery[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, User)

