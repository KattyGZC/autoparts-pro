from uuid import UUID
from app.domain.enums import RepairOrderStatus
from app.adapters.schemas.base import BaseSchema

class RepairOrderBase(BaseSchema):
    vehicle_id: UUID
    status: RepairOrderStatus
    labor_cost: float

class RepairOrderCreate(RepairOrderBase):
    pass

class RepairOrderUpdate(RepairOrderBase):
    pass

class RepairOrderRead(RepairOrderBase):
    id: UUID
