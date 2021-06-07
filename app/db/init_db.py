from sqlalchemy.orm import Session

from app import crud, schemas
from app import models  # noqa: F401
from app.core.config import settings
from app.db.base import Base


# make sure all SQL Alchemy models are imported (app.models) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly


def init_db(db: Session) -> None:
    from app.db.session import engine

    # Tables should be created with Alembic migrations, but for this sample
    # project we'll just use SQLAlchemy ORM to create the tables for simplicity
    Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
