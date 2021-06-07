from faker.proxy import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate


def test_create_user(db: Session, faker: Faker) -> None:
    email = faker.email()
    password = faker.password()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email
    assert user.hashed_password is not None


def test_get_user(db: Session, faker: Faker) -> None:
    email = faker.email()
    full_name = faker.name()
    user_in = UserCreate(email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_authenticate_user(db: Session, faker: Faker) -> None:
    email = faker.email()
    password = faker.password()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session, faker: Faker) -> None:
    email = faker.email()
    password = faker.password()
    user = crud.user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session, faker: Faker) -> None:
    email = faker.email()
    password = faker.password()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session, faker: Faker) -> None:
    email = faker.email()
    password = faker.password()
    user_in = UserCreate(email=email, password=password, disabled=True)
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active


def test_check_if_user_is_superuser(db: Session, faker: Faker) -> None:
    email = faker.email()
    password = faker.password()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session, faker: Faker) -> None:
    username = faker.email()
    password = faker.password()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user(db: Session, faker: Faker) -> None:
    password = faker.password()
    username = faker.email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session, faker: Faker) -> None:
    password = faker.password()
    email = faker.email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    new_password = faker.password()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
