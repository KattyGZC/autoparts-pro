from pydantic import BaseModel
from uuid import UUID
from app.adapters.schemas.customer import CustomerSimpleResponse
from app.adapters.schemas.vehicle import VehicleSimpleResponse

class OptimizedRepairOrderResponse(BaseModel):
    repair_order_id: UUID
    customer: CustomerSimpleResponse
    vehicle: VehicleSimpleResponse
    total_cost_repair: float
    expected_profit: float
