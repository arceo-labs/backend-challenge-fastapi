from sqlalchemy import Boolean, Column, Integer, String

from app.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r})"
