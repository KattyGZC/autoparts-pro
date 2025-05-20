from uuid import UUID
from app.domain.enums import RepairOrderStatus
from app.adapters.schemas.base import BaseSchema
from app.adapters.schemas.repair_order_part import RepairOrderPartRequest
from app.adapters.schemas.customer import CustomerSimpleResponse
from app.adapters.schemas.vehicle import VehicleSimpleResponse
from datetime import datetime
from typing import Optional

class RepairOrderBase(BaseSchema):
    status: RepairOrderStatus
    labor_cost: float
    date_expected_out: Optional[datetime]
    date_out: Optional[datetime]
    total_cost_repair: float

class RepairOrderCreate(BaseSchema):
    vehicle_id: UUID
    customer_id: UUID

class RepairOrderUpdate(RepairOrderBase):
    parts: Optional[list[RepairOrderPartRequest]] = None

class RepairOrderRead(RepairOrderBase):
    id: UUID
    vehicle: VehicleSimpleResponse
    customer: CustomerSimpleResponse
    date_in: datetime

class RepairOrderUpdateStatusRequest(BaseSchema):
    status: RepairOrderStatus
