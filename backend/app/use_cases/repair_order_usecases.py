from app.domain.models import RepairOrder
from app.domain.enums import RepairOrderStatus
from app.domain.exceptions import (
    RepairOrderNotFoundException,
    RepairOrderValidationException,
    VehicleNotFoundException,
    CustomerNotFoundException,
)

from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
from uuid import UUID
import uuid
from app.adapters.schemas.repair_order import RepairOrderCreate, RepairOrderRead, RepairOrderUpdate

class RepairOrderUseCase:
    def __init__(self,
                 repair_order_repo: RepairOrderRepository,
                 vehicle_repo: VehicleRepository,
                 customer_repo: CustomerRepository):
        self.repair_order_repo = repair_order_repo
        self.vehicle_repo = vehicle_repo
        self.customer_repo = customer_repo

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
            is_active=repair_order.is_active,
            status=repair_order.status,
            labor_cost=repair_order.labor_cost,
            date_in=repair_order.date_in,
            date_expected_out=repair_order.date_expected_out,
            date_out=repair_order.date_out
        )
        orm_repair_order = self.repair_order_repo.add(new_repair_order)
        return RepairOrderRead.model_validate(orm_repair_order)

    def get_repair_order_by_id(self, repair_order_id: uuid.UUID) -> RepairOrderRead:
        repair_order = self.repair_order_repo.get_by_id(repair_order_id)
        if not repair_order:
            raise RepairOrderNotFoundException(repair_order_id)
        return RepairOrderRead.model_validate(repair_order)

    def get_all_repair_orders(self) -> list[RepairOrderRead]:
        return [RepairOrderRead.model_validate(order) for order in self.repair_order_repo.get_all()]

   
    def update_repair_order(self, repair_order_id: uuid.UUID, data: RepairOrderUpdate) -> RepairOrderRead:
        self._validate_repair_order(data)
        updated_repair_order = self.repair_order_repo.update(repair_order_id, data.model_dump(exclude_unset=True))
        if not updated_repair_order:
            raise RepairOrderNotFoundException(repair_order_id)
        return RepairOrderRead.model_validate(updated_repair_order)

    def _validate_repair_order(self, repair_order: RepairOrderCreate | RepairOrderUpdate):
        if repair_order.labor_cost < 0:
            raise RepairOrderValidationException("Labor cost cannot be negative.")
        if repair_order.status not in [item.value for item in RepairOrderStatus]:
            raise RepairOrderValidationException(f"Invalid status: {repair_order.status}")

    def get_repair_orders_by_vehicle_id(self, vehicle_id: uuid.UUID) -> list[RepairOrderRead]:
        repair_orders = self.repair_order_repo.get_by_vehicle_id(vehicle_id)
        return [RepairOrderRead.model_validate(order) for order in repair_orders]
        