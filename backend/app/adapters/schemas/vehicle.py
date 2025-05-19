from uuid import UUID
from app.adapters.schemas.base import BaseSchema

class VehicleBase(BaseSchema):
    license_plate: str
    model: str
    brand: str
    year: int
    color: str
    is_active: bool = True

class VehicleCreate(VehicleBase):
    customer_id: UUID

class VehicleUpdate(VehicleBase):
    customer_id: UUID

class VehicleRead(VehicleBase):
    id: UUID
    customer_id: UUID
    is_active: bool