from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.infrastructure.db.models import RepairOrderPart as RepairOrderPartORM
from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.models import RepairOrderPart

class RepairOrderPartRepository(BaseRepository[RepairOrderPartORM]):
    def __init__(self, db: Session):
        super().__init__(db, RepairOrderPartORM)

    def get_by_id(self, id: UUID) -> Optional[RepairOrderPartORM]:
        return super().get_by_id(id)

    def get_all(self) -> list[RepairOrderPartORM]:
        return super().get_all()

    def add(self, repair_order_part: RepairOrderPart) -> RepairOrderPart:
        orm_repair_order_part = RepairOrderPartORM(
            id=repair_order_part.id,
            repair_order_id=repair_order_part.repair_order_id,
            part_id=repair_order_part.part_id,
            quantity=repair_order_part.quantity,
            is_active=repair_order_part.is_active,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db_obj = super().add(orm_repair_order_part)
        return RepairOrderPart(
            id=db_obj.id,
            repair_order_id=db_obj.repair_order_id,
            part_id=db_obj.part_id,
            quantity=db_obj.quantity,
            is_active=db_obj.is_active,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )

    def update(self, id: UUID, updates: dict) -> RepairOrderPart | None:
        return super().update(id, updates)

    def get_by_order_and_part(self, order_id: UUID, part_id: UUID) -> Optional[RepairOrderPart]:
        return (
            self.db.query(self.model)
            .filter(
                self.model.repair_order_id == order_id,
                self.model.part_id == part_id,
                self.model.is_active == True
            )
            .first()
        )

    def get_by_order_id(self, order_id: UUID) -> list[RepairOrderPart]:
        return (
            self.db.query(self.model)
            .filter(
                self.model.repair_order_id == order_id,
                self.model.is_active == True
            )
            .all()
        )

    def get_all_by_order_id(self, repair_order_id: UUID) -> list[RepairOrderPart]:
        return (
            self.db.query(self.model)
            .filter(self.model.repair_order_id == repair_order_id)
            .filter(self.model.is_active == True)
            .all()
        )

    def delete(self, id: UUID) -> bool:
        return super().disable(id)
