from app.infrastructure.db.models import InventoryPart as InventoryPartORM
from sqlalchemy.orm import Session
from uuid import UUID
from app.domain.models import InventoryPart
from app.infrastructure.repositories.base_repository import BaseRepository
from typing import Optional


class InventoryPartRepository(BaseRepository[InventoryPartORM]):
    def __init__(self, db_session: Session):
        super().__init__(db_session, InventoryPartORM)

    def get_all(self) -> list[InventoryPart]:
        return super().get_all()

    def get_by_id(self, id: UUID) -> Optional[InventoryPart]:
        return super().get_by_id(id)

    def get_by_name(self, name: str) -> Optional[InventoryPart]:
        return self.db.query(self.model).filter(self.model.name == name).first()

    def add(self, inventory_part: InventoryPart) -> InventoryPart:
        orm_inventory_part = InventoryPartORM(
            id=inventory_part.id,
            name=inventory_part.name,
            description=inventory_part.description,
            stock_quantity=inventory_part.stock_quantity,
            cost=inventory_part.cost,
            is_active=inventory_part.is_active,
        )
        db_obj = super().add(orm_inventory_part)
        return InventoryPart(
            id=db_obj.id,
            name=db_obj.name,
            description=db_obj.description,
            stock_quantity=db_obj.stock_quantity,
            cost=db_obj.cost,
            is_active=db_obj.is_active,
        )

    def update(self, id: UUID, updated_data: dict) -> Optional[InventoryPart]:
        return super().update(id, updated_data)

    def disable(self, id: UUID) -> bool:
        return super().disable(id)
        