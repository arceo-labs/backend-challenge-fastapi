from app.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import create_session
from fastapi import FastAPI

app = FastAPI(title="Magazine Subscription Service")
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    with create_session() as db:
        init_db(db)


if __name__ == "__main__":
    import uvicorn

    # Start the webserver
    uvicorn.run(
        app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        debug=settings.DEBUG,
    )
