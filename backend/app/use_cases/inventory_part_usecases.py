from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.domain.models import InventoryPart
from app.adapters.schemas.inventory_part import InventoryPartCreate, InventoryPartUpdate, InventoryPartRead
from app.domain.exceptions import InventoryPartDuplicateException, InventoryPartNotFoundException
from typing import Optional
import uuid

class InventoryPartUseCase:
    def __init__(self, repository: InventoryPartRepository):
        self.repository = repository

    def create_inventory_part(self, inventory_part_data: InventoryPartCreate) -> InventoryPartRead:
        if inventory_part_data.name and self.repository.get_by_name(inventory_part_data.name):
            raise InventoryPartDuplicateException("name", inventory_part_data.name)
        new_inventory_part = InventoryPart(
            id=uuid.uuid4(),
            name=inventory_part_data.name,
            description=inventory_part_data.description,
            stock_quantity=inventory_part_data.stock_quantity,
            cost=inventory_part_data.cost,
            final_price=inventory_part_data.final_price,
            is_active=True,
        )
        orm_inventory_part = self.repository.add(new_inventory_part)
        return InventoryPartRead.model_validate(orm_inventory_part)
        
    
    def get_all_inventory_parts(self) -> list[InventoryPart]:
        return self.repository.get_all()

    def get_inventory_part_by_id(self, inventory_part_id: uuid.UUID) -> Optional[InventoryPart]:
        inventory_part = self.repository.get_by_id(inventory_part_id)
        if not inventory_part:
            raise InventoryPartNotFoundException(inventory_part_id)
        return InventoryPartRead.model_validate(inventory_part)

    def update_inventory_part(self, inventory_part_id: uuid.UUID, inventory_part_data: InventoryPartUpdate) -> Optional[InventoryPart]:
        updated_inventory_part = self.repository.update(inventory_part_id, inventory_part_data.model_dump(exclude_unset=True))
        if not updated_inventory_part:
            raise InventoryPartNotFoundException(inventory_part_id)
        return InventoryPartRead.model_validate(updated_inventory_part)

    def disable_inventory_part(self, inventory_part_id: uuid.UUID) -> bool:
        return self.repository.disable(inventory_part_id)
        