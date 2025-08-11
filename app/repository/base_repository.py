from typing import Type, TypeVar, Generic, Optional, Union

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# 定义泛型
T = TypeVar("T", bound="DatabaseBaseModel")


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get(self, data_id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == data_id).first()

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def create(self, data: Union[T, PydanticBaseModel, dict]) -> T:
        try:
            if isinstance(data, PydanticBaseModel):
                data = self.model(**data.dict(exclude_unset=True))
            elif isinstance(data, dict):
                data = self.model(**data)
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            return data
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update(self, data_id: int, data: Union[PydanticBaseModel, dict]) -> Optional[T]:
        try:
            if isinstance(data, PydanticBaseModel):
                data = data.dict(exclude_unset=True)
            self.db.query(self.model).filter(self.model.id == data_id).update(data)
            self.db.commit()
            return self.get(data_id)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, data_id: int) -> None:
        try:
            self.db.query(self.model).filter(self.model.id == data_id).delete()
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
