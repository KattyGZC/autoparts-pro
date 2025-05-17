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

@dataclass
class Vehicle:
    id: UUID
    customer_id: UUID
    license_plate: str
    model: str
    brand: str
    year: int

@dataclass
class Part:
    id: UUID
    name: str
    description: Optional[str]
    stock_quantity: int
    cost: float

@dataclass
class RepairOrder:
    id: UUID
    vehicle_id: UUID
    status: RepairOrderStatus
    labor_cost: float

@dataclass
class RepairOrderPart:
    id: UUID
    repair_order_id: UUID
    part_id: UUID
    quantity: int
