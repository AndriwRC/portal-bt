from fastapi import FastAPI
from .features.users.routes import router as users_router
from .features.auth.routes import router as auth_router
from .features.schools.routes import router as schools_router
from .features.visits.routes import router as visits_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(schools_router)
    app.include_router(visits_router)
