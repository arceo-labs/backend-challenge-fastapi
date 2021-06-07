import secrets
from typing import Optional

from pydantic import BaseSettings, EmailStr, SecretStr, validator
import tempfile
import atexit


class Settings(BaseSettings):
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8080
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = None

    @validator("SQLALCHEMY_DATABASE_URI")
    def default_to_tmp_db(cls, v):
        if v is not None:
            return v

        dbfile = tempfile.NamedTemporaryFile(suffix=".sqlite3")
        atexit.register(dbfile.close)
        return f"sqlite:///{dbfile.name}"

    SECRET_KEY: SecretStr = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Inlining values for simplicity - DO NOT DO THIS IN A PRODUCTION APP!
    FIRST_SUPERUSER: EmailStr = "admin@arceo.ai"
    FIRST_SUPERUSER_PASSWORD: SecretStr = "admin"


settings = Settings()
