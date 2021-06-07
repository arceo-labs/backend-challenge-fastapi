from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_db, get_current_active_superuser, get_current_active_user

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    dependencies=[Depends(get_current_active_superuser)],
    response_model=schemas.User,
)
async def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create new user.

    This endpoint can only be accessed by an active superuser.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get(
    "/",
    response_model=List[schemas.User],
)
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve users.

    * Superusers can list all users
    * Normal users can only list themselves
    """
    if current_user.is_superuser:
        return crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        return [current_user][skip:limit]


@router.get(
    "/{user_id}",
    dependencies=[],
    response_model=List[schemas.User],
)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve a user.

    Users can only be fetched for themselves or by a superuser.
    """
    if not (current_user.is_superuser or user_id == current_user.id):
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="A user was not found with that id."
        )
    return user
