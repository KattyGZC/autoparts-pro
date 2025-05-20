from uuid import UUID
from app.adapters.schemas.base import BaseSchema

class RepairOrderPartBase(BaseSchema):
    quantity: int

class RepairOrderPartCreate(RepairOrderPartBase):
    repair_order_id: UUID
    part_id: UUID

class RepairOrderPartUpdate(RepairOrderPartBase):
    pass

class RepairOrderPartRead(RepairOrderPartBase):
    id: UUID
    repair_order_id: UUID
    part_id: UUID

class RepairOrderPartRequest(RepairOrderPartBase):
    part_id: UUID
