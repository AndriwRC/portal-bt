from sqlmodel import Session
from app.core.models import BaseQuery
from .models import User


class UserQueries(BaseQuery[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

