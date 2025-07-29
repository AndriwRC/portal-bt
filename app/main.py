from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database.core import init_db
from .api import register_routes
from .features.hours import models
from .features.visits import models
from .features.schools import models
from .features.parameters import models


@asynccontextmanager
async def create_db(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=create_db)
register_routes(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
