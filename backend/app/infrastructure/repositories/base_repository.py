from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db_session: Session, model: Type[T]):
        self.db = db_session
        self.model = model

    def get_by_id(self, id: str) -> Optional[T]:
        return (self.db.query(self.model)
                .filter(self.model.id == id)
                .first())

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def add(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def disable(self, id: str) -> bool:
        obj = self.get_by_id(id)
        if not obj:
            return False
        setattr(obj, "is_active", False)
        self.db.commit()
        return True

    def update(self, id: str, updated_data: dict) -> Optional[T]:
        obj = self.get_by_id(id)
        if not obj:
            return None
        for key, value in updated_data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj
        