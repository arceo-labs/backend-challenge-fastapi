from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date, datetime

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = self._encode_obj_in(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = self._encode_obj_in(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    @classmethod
    def _encode_obj_in(
        cls,
        obj_in: Union[ModelType, CreateSchemaType, UpdateSchemaType, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Prepare an object for serialization to the database.

        HACK[SQLite3]: Leave Date and Datetime objects alone, as SQlite cannot handle strings for dates
        """
        if isinstance(obj_in, BaseModel):
            kv_iter = obj_in
        elif isinstance(obj_in, Base):
            kv_iter = [
                (k, v) for k, v in obj_in.__dict__.items() if not k.startswith("_")
            ]
        elif isinstance(obj_in, dict):
            kv_iter = obj_in.items()
        else:
            raise ValueError(f"Unsupported type for obj_in value: {obj_in!r}")

        obj_in_data = {}
        for field, value in kv_iter:
            if isinstance(value, (date, datetime)):
                obj_in_data[field] = value
            else:
                obj_in_data[field] = jsonable_encoder(value)
        return obj_in_data
