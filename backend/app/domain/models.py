from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from app.domain.enums import RepairOrderStatus

@dataclass
class Customer:
    id: UUID
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    is_active: bool

@dataclass
class Vehicle:
    id: UUID
    customer_id: UUID
    license_plate: str
    model: str
    brand: str
    year: int
    color: str
    is_active: bool

@dataclass
class InventoryPart:
    id: UUID
    name: str
    description: Optional[str]
    stock_quantity: int
    cost: float
    is_active: bool

@dataclass
class RepairOrder:
    id: UUID
    vehicle_id: UUID
    status: RepairOrderStatus
    labor_cost: float
    is_active: bool

@dataclass
class RepairOrderPart:
    id: UUID
    repair_order_id: UUID
    part_id: UUID
    quantity: int
    is_active: bool
