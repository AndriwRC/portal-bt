from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.database.connection import Connection


def get_session():
    with Session(Connection.ENGINE) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
