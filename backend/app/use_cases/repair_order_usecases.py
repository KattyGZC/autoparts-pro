from app.domain.models import RepairOrder
from app.domain.enums import RepairOrderStatus
from app.domain.exceptions import (
    RepairOrderNotFoundException,
    RepairOrderValidationException,
    VehicleNotFoundException,
    CustomerNotFoundException
)
from app.adapters.schemas.repair_order import RepairOrderUpdateStatusRequest
from app.infrastructure.repositories.repair_order_part_repository import RepairOrderPartRepository
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
from uuid import UUID
import uuid
from app.adapters.schemas.repair_order import RepairOrderCreate, RepairOrderRead, RepairOrderUpdate
from app.adapters.schemas.inventory_part import PartDetailByInventoryPart
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.use_cases.repair_order_part_usecases import RepairOrderPartUseCase

class RepairOrderUseCase:
    def __init__(self,
                 repair_order_repo: RepairOrderRepository,
                 vehicle_repo: VehicleRepository,
                 customer_repo: CustomerRepository,
                 inventory_part_repo: InventoryPartRepository,
                 repair_order_part_usecase: RepairOrderPartUseCase,
                 repair_order_part_repo: RepairOrderPartRepository):
        self.repair_order_repo = repair_order_repo
        self.vehicle_repo = vehicle_repo
        self.customer_repo = customer_repo
        self.inventory_part_repo = inventory_part_repo
        self.repair_order_part_usecase = repair_order_part_usecase
        self.repair_order_part_repo = repair_order_part_repo

    def create_repair_order(self, repair_order: RepairOrderCreate) -> RepairOrderRead:
        if not repair_order.customer_id:
            raise RepairOrderValidationException("Customer ID is required.")
        if not repair_order.vehicle_id:
            raise RepairOrderValidationException("Vehicle ID is required.") 
        self._validate_repair_order(repair_order)
        if not self.vehicle_repo.get_by_id(repair_order.vehicle_id):
            raise VehicleNotFoundException(repair_order.vehicle_id)
        if not self.customer_repo.get_by_id(repair_order.customer_id):
            raise CustomerNotFoundException(repair_order.customer_id)
        
        new_repair_order = RepairOrder(
            id=uuid.uuid4(),
            vehicle_id=repair_order.vehicle_id,
            customer_id=repair_order.customer_id,
            is_active=True,
            status=RepairOrderStatus.PENDING
        )
        orm_repair_order = self.repair_order_repo.add(new_repair_order)
        return RepairOrderRead.model_validate(orm_repair_order)

    def get_repair_order_by_id(self, repair_order_id: UUID) -> RepairOrderRead:
        repair_order = self.repair_order_repo.get_by_id(repair_order_id)
        if not repair_order:
            raise RepairOrderNotFoundException(repair_order_id)
        return RepairOrderRead.model_validate(repair_order)

    def get_all_repair_orders(self) -> list[RepairOrderRead]:
        return [RepairOrderRead.model_validate(order) for order in self.repair_order_repo.get_all()]
   
    def update_repair_order(self, repair_order_id: UUID, data: RepairOrderUpdate) -> RepairOrderRead:
        self._validate_repair_order(data)

        existing_order = self.repair_order_repo.get_by_id(repair_order_id)
        if not existing_order:
            raise RepairOrderNotFoundException(repair_order_id)

        current_status = existing_order.status
        next_status = data.status
        self._validate_status_transition(current_status, next_status)

        total_parts_cost = 0
        if data.parts:
            total_parts_cost = self.repair_order_part_usecase.sync_parts_for_order(
                repair_order_id=repair_order_id,
                incoming_parts=data.parts
            )

        total_cost = data.labor_cost + total_parts_cost
        update_payload = data.model_dump(exclude_unset=True)
        update_payload["total_cost_repair"] = total_cost
        update_payload.pop("parts", None)

        updated_order = self.repair_order_repo.update(repair_order_id, update_payload)
        return RepairOrderRead.model_validate(updated_order)

    def update_repair_order_status(self, repair_order_id: UUID, data: RepairOrderUpdateStatusRequest) -> RepairOrderRead:
        existing_order = self.repair_order_repo.get_by_id(repair_order_id)
        if not existing_order:
            raise RepairOrderNotFoundException(repair_order_id)
        
        self._validate_status_transition(existing_order.status, data.status)
        update_payload = data.model_dump(exclude_unset=True)
        updated_order = self.repair_order_repo.update(repair_order_id, update_payload)
        return RepairOrderRead.model_validate(updated_order)

    def _validate_status_transition(self, current_status: RepairOrderStatus, next_status: RepairOrderStatus):
        valid_transitions = {
            "pending": ["in_progress", "canceled"],
            "in_progress": ["completed", "canceled"],
        }

        if current_status in ["completed", "canceled"]:
            raise RepairOrderValidationException("Completed or canceled orders cannot be modified.")
        
        if next_status not in valid_transitions.get(current_status.value, []):
            raise RepairOrderValidationException(
                f"Cannot change status from {current_status.value} to {next_status.value}.")

    def _validate_repair_order(self, repair_order: RepairOrderCreate | RepairOrderUpdate):
        if repair_order.labor_cost < 0:
            raise RepairOrderValidationException("Labor cost cannot be negative.")
        if repair_order.status not in [item.value for item in RepairOrderStatus]:
            raise RepairOrderValidationException(f"Invalid status: {repair_order.status}")

    def get_repair_orders_by_vehicle_id(self, vehicle_id: uuid.UUID) -> list[RepairOrderRead]:
        repair_orders = self.repair_order_repo.get_by_vehicle_id(vehicle_id)
        return [RepairOrderRead.model_validate(order) for order in repair_orders]

    def get_parts_used_in_order(self, repair_order_id: UUID) -> list[PartDetailByInventoryPart]:
        order = self.repair_order_repo.get_by_id(repair_order_id)
        if not order:
            raise RepairOrderNotFoundException(repair_order_id)

        relations = self.repair_order_part_repo.get_all_by_order_id(repair_order_id)
        
        result = []
        for rel in relations:
            part = self.inventory_part_repo.get_by_id(rel.part_id)
            if not part:
                continue  
            result.append(PartDetailByInventoryPart(
                id=part.id,
                name=part.name,
                description=part.description,
                cost=part.cost,
                final_price=part.final_price,
                quantity_used=rel.quantity
            ))
        return result
        