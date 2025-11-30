from sqlmodel import create_engine
from ..core.settings import settings


class Connection:
    DB_URI = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    ENGINE = create_engine(url=DB_URI, echo=settings.DB_ECHO)
