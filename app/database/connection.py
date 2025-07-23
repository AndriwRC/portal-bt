from sqlmodel import create_engine
from ..config.settings import Settings


class Connection:
    DB_URI = f"postgresql+psycopg2://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}"
    ENGINE = create_engine(url=DB_URI, echo=True)
