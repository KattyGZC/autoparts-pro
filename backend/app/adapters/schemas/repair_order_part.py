from uuid import UUID
from app.adapters.schemas.base import BaseSchema

class RepairOrderPartBase(BaseSchema):
    quantity: int
    is_active: bool

class RepairOrderPartCreate(RepairOrderPartBase):
    repair_order_id: UUID
    part_id: UUID

class RepairOrderPartUpdate(RepairOrderPartBase):
    pass

class RepairOrderPartRead(RepairOrderPartBase):
    id: UUID
    repair_order_id: UUID
    part_id: UUID
