from uuid import UUID
from app.adapters.schemas.base import BaseSchema

class RepairOrderPartBase(BaseSchema):
    repair_order_id: UUID
    part_id: UUID
    quantity: int

class RepairOrderPartCreate(RepairOrderPartBase):
    pass

class RepairOrderPartUpdate(RepairOrderPartBase):
    pass

class RepairOrderPartRead(RepairOrderPartBase):
    id: UUID
