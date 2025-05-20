from uuid import UUID
from app.domain.enums import RepairOrderStatus
from app.adapters.schemas.base import BaseSchema
from datetime import datetime
from typing import Optional

class RepairOrderBase(BaseSchema):
    status: RepairOrderStatus
    labor_cost: float
    date_expected_out: Optional[datetime]
    date_out: Optional[datetime]
    is_active: bool

class RepairOrderCreate(RepairOrderBase):
    vehicle_id: UUID
    customer_id: UUID
    date_in: datetime

class RepairOrderUpdate(RepairOrderBase):
    pass

class RepairOrderRead(RepairOrderBase):
    id: UUID
    vehicle_id: UUID
    customer_id: UUID
    date_in: datetime
