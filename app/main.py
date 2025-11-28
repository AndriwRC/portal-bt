from fastapi import FastAPI
from sqlmodel import Session
from contextlib import asynccontextmanager

from .api import register_routes
from .database.core import init_db, Connection
from .database.seeders.startup import sync_permissions, sync_roles

from .features.hours import models
from .features.visits import models
from .features.schools import models
from .features.parameters import models


@asynccontextmanager
async def create_db(app: FastAPI):
    init_db()
    with Session(Connection.ENGINE) as session:
        sync_permissions(session)
        sync_roles(session)

    yield


app = FastAPI(lifespan=create_db)
register_routes(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
