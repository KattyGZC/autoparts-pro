from app.infrastructure.repositories.repair_order_part_repository import RepairOrderPartRepository
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
import uuid
from app.domain.models import RepairOrderPart
from app.adapters.schemas.repair_order_part import RepairOrderPartCreate, RepairOrderPartRead, RepairOrderPartUpdate
from app.domain.exceptions import (
    RepairOrderPartNotFoundException,
    RepairOrderPartValidationException,
    RepairOrderNotFoundException,
    InventoryPartNotFoundException,
)
from datetime import datetime

class RepairOrderPartUseCase:
    def __init__(self,
                 repair_order_part_repo: RepairOrderPartRepository,
                 repair_order_repo: RepairOrderRepository,
                 part_repo: InventoryPartRepository):
        self.repair_order_part_repo = repair_order_part_repo
        self.repair_order_repo = repair_order_repo
        self.part_repo = part_repo

    def create_repair_order_part(self, repair_order_part: RepairOrderPartCreate) -> RepairOrderPartRead:
        if repair_order_part.quantity <= 0:
            raise RepairOrderPartValidationException("Quantity must be greater than zero.")
        if not repair_order_part.repair_order_id:
            raise RepairOrderPartValidationException("Repair order ID is required.")
        if not repair_order_part.part_id:
            raise RepairOrderPartValidationException("Part ID is required.")
        if not self.repair_order_repo.get_by_id(repair_order_part.repair_order_id):
            raise RepairOrderNotFoundException(repair_order_part.repair_order_id)
        if not self.part_repo.get_by_id(repair_order_part.part_id):
            raise InventoryPartNotFoundException(repair_order_part.part_id)

        new_repair_order_part = RepairOrderPart(
            id=uuid.uuid4(),
            repair_order_id=repair_order_part.repair_order_id,
            part_id=repair_order_part.part_id,
            quantity=repair_order_part.quantity,
            is_active=repair_order_part.is_active,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        orm_repair_order_part = self.repair_order_part_repo.add(new_repair_order_part)
        return RepairOrderPartRead.model_validate(orm_repair_order_part)

    def get_repair_order_part_by_id(self, repair_order_part_id: uuid.UUID) -> RepairOrderPartRead:
        repair_order_part = self.repair_order_part_repo.get_by_id(repair_order_part_id)
        if not repair_order_part:
            raise RepairOrderPartNotFoundException(repair_order_part_id)
        return RepairOrderPartRead.model_validate(repair_order_part)

    def get_all_repair_order_parts(self) -> list[RepairOrderPartRead]:
        return [RepairOrderPartRead.model_validate(order) for order in self.repair_order_part_repo.get_all()]

   
    def update_repair_order_part(self, repair_order_part_id: uuid.UUID, data: RepairOrderPartUpdate) -> RepairOrderPartRead:
        if data.quantity <= 0:
            raise RepairOrderPartValidationException("Quantity must be greater than zero.")

        updated_repair_order_part = self.repair_order_part_repo.update(repair_order_part_id, data.model_dump(exclude_unset=True))
        if not updated_repair_order_part:
            raise RepairOrderPartNotFoundException(repair_order_part_id)
        return RepairOrderPartRead.model_validate(updated_repair_order_part)
