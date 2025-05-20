from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from app.domain.enums import RepairOrderStatus
from datetime import datetime
from dataclasses import field
from datetime import timezone

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
    customer_id: UUID
    status: RepairOrderStatus
    labor_cost: float
    date_in: Optional[datetime]
    date_expected_out: Optional[datetime]
    date_out: Optional[datetime]
    total_cost_repair: float
    is_active: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class RepairOrderPart:
    id: UUID
    repair_order_id: UUID
    part_id: UUID
    quantity: int
    is_active: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    