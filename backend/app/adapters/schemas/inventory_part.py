from uuid import UUID
from typing import Optional
from app.adapters.schemas.base import BaseSchema

class PartBase(BaseSchema):
    name: str
    description: Optional[str] = None
    stock_quantity: int
    cost: float

class PartCreate(PartBase):
    pass

class PartUpdate(PartBase):
    pass

class PartRead(PartBase):
    id: UUID
