from fastapi import FastAPI
from .features.auth.routes import router as auth_router
from .features.hours.routes import router as hours_router
from .features.users.routes import router as users_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(hours_router)
    app.include_router(users_router)
