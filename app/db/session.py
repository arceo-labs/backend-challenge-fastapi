from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    future=True,
    connect_args={"check_same_thread": False},
)


def create_session():
    return Session(engine)
