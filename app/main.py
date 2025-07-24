from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database.core import init_db
from .features.user import models

@asynccontextmanager
async def create_db(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=create_db)


@app.get("/")
def read_root():
    return {"Hello": "World"}
