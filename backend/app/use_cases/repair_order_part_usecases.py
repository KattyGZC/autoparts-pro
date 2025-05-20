from app.infrastructure.repositories.repair_order_part_repository import RepairOrderPartRepository
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
import uuid
from uuid import UUID
from app.domain.models import RepairOrderPart
from app.adapters.schemas.repair_order_part import RepairOrderPartCreate, RepairOrderPartRead, RepairOrderPartUpdate, RepairOrderPartRequest
from app.domain.exceptions import (
    RepairOrderPartNotFoundException,
    RepairOrderPartValidationException,
    RepairOrderNotFoundException,
    InventoryPartNotFoundException,
    InventoryPartValidationException,
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

    def get_repair_order_part_by_id(self, repair_order_part_id: UUID) -> RepairOrderPartRead:
        repair_order_part = self.repair_order_part_repo.get_by_id(repair_order_part_id)
        if not repair_order_part:
            raise RepairOrderPartNotFoundException(repair_order_part_id)
        return RepairOrderPartRead.model_validate(repair_order_part)

    def get_all_repair_order_parts(self) -> list[RepairOrderPartRead]:
        return [RepairOrderPartRead.model_validate(order) for order in self.repair_order_part_repo.get_all()]

   
    def update_repair_order_part(self, repair_order_part_id: UUID, data: RepairOrderPartUpdate) -> RepairOrderPartRead:
        if data.quantity <= 0:
            raise RepairOrderPartValidationException("Quantity must be greater than zero.")

        updated_repair_order_part = self.repair_order_part_repo.update(repair_order_part_id, data.model_dump(exclude_unset=True))
        if not updated_repair_order_part:
            raise RepairOrderPartNotFoundException(repair_order_part_id)
        return RepairOrderPartRead.model_validate(updated_repair_order_part)

    def sync_parts_for_order(self, repair_order_id: UUID, incoming_parts: list[RepairOrderPartRequest]) -> float:
        "Sync parts for order"
        total_cost = 0.0

        existing_parts = self.repair_order_part_repo.get_by_order_id(repair_order_id)
        existing_parts_dict = {p.part_id: p for p in existing_parts}
        incoming_parts_dict = {p.part_id: p for p in incoming_parts}
        for part_input in incoming_parts:
            part_id = part_input.part_id
            part = self.part_repo.get_by_id(part_id)
            if not part:
                raise InventoryPartNotFoundException(part_id)

            existing_relation = existing_parts_dict.get(part_id)

            if existing_relation:
                quantity_diff = part_input.quantity - existing_relation.quantity
                new_stock = part.stock_quantity - quantity_diff
                if new_stock < 0:
                    raise InventoryPartValidationException(
                        f"Not enough stock for part {part.name}. Needed diff: {quantity_diff}, available: {part.stock_quantity}"
                    )

                self.repair_order_part_repo.update(
                    existing_relation.id, {"quantity": part_input.quantity}
                )
                self.part_repo.update(part.id, {"stock_quantity": new_stock})
            else:
                if part.stock_quantity < part_input.quantity:
                    raise InventoryPartValidationException(
                        f"Not enough stock for part {part.name}. Available: {part.stock_quantity}, requested: {part_input.quantity}"
                    )

                part_relation = RepairOrderPart(
                    repair_order_id=repair_order_id,
                    part_id=part_input.part_id,
                    quantity=part_input.quantity
                )
                self.repair_order_part_repo.add(part_relation)

                self.part_repo.update(
                    part.id, {"stock_quantity": part.stock_quantity - part_input.quantity}
                )

            total_cost += part.cost * part_input.quantity

        for existing in existing_parts:
            if existing.part_id not in incoming_parts_dict:
                part = self.part_repo.get_by_id(existing.part_id)
                if part:
                    self.part_repo.update(
                        part.id, {"stock_quantity": part.stock_quantity + existing.quantity}
                    )
                self.repair_order_part_repo.delete(existing.id)

        return total_cost
