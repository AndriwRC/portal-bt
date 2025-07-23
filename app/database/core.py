from fastapi import Depends
from sqlmodel import SQLModel, Session
from typing import Annotated

from .connection import Connection


def init_db():
    SQLModel.metadata.create_all(Connection.ENGINE)


def get_session():
    with Session(Connection.ENGINE) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
