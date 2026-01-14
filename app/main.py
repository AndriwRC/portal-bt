from fastapi import FastAPI

from .api import register_routes
from .database.models import *


app = FastAPI()
register_routes(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
