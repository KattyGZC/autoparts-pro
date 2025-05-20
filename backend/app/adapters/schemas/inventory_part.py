from uuid import UUID
from typing import Optional
from app.adapters.schemas.base import BaseSchema

class InventoryPartBase(BaseSchema):
    name: str
    description: Optional[str] = None
    stock_quantity: int
    cost: float
    final_price: float

class InventoryPartCreate(InventoryPartBase):
    pass

class InventoryPartUpdate(InventoryPartBase):
    pass

class InventoryPartRead(InventoryPartBase):
    id: UUID

class PartDetailByInventoryPart(BaseSchema):
    id: UUID
    name: str
    description: Optional[str] = None
    cost: float
    final_price: float
    quantity_used: int
