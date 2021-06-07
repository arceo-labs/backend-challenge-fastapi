from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import get_db

router = APIRouter()


@router.get("/", response_model=schemas.Healthcheck)
async def healthcheck(db: Session = Depends(get_db)):
    """
    Test the health of the service (e.g. - DB connectivity, etc.)
    """
    try:
        db.execute("SELECT 1")
    except Exception as e:
        return schemas.Healthcheck(healthy=False, errors=[str(e)])
    else:
        return schemas.Healthcheck(healthy=True)
