from typing import Dict, Generator
from unittest import mock

import pytest
from faker.proxy import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import create_session
from app.main import app


@pytest.fixture
def db(tmpdir, monkeypatch) -> Generator:
    """Creates a new, temporary DB for each individual test"""
    db_uri = f"sqlite:///{str(tmpdir / 'db.sqlite3')}"
    engine = create_engine(
        db_uri, future=True, connect_args={"check_same_thread": False}
    )
    with mock.patch("app.db.session.engine", engine), create_session() as db:
        init_db(db)
        yield db


@pytest.fixture
def client(db) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return _get_user_authentication_headers(
        client=client,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD.get_secret_value(),
    )


@pytest.fixture
def normal_user_token_headers(
    client: TestClient, db: Session, faker: Faker
) -> Dict[str, str]:
    email = faker.email()
    password = faker.password()
    user = crud.user.get_by_email(db, email=email)
    if user:
        crud.user.update(db, db_obj=user, obj_in=schemas.UserUpdate(password=password))
    else:
        crud.user.create(
            db,
            obj_in=schemas.UserCreate(
                email=email, password=password, full_name=faker.name()
            ),
        )
    return _get_user_authentication_headers(
        client=client, email=email, password=password
    )


def _get_user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
