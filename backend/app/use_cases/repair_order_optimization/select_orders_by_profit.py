from typing import List
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.adapters.schemas.repair_order_optimization import OptimizedRepairOrderResponse
from app.adapters.schemas.customer import CustomerSimpleResponse
from app.adapters.schemas.vehicle import VehicleSimpleResponse
from app.domain.exceptions import NoAvailableRepairOrdersException, InvalidRepairOrderDataException
from .validate_order_inventory import is_order_fulfillable
from .calculate_order_profit import calculate_order_profit


class SelectRepairOrdersByProfitUseCase:
    def __init__(
        self,
        repair_order_repository: RepairOrderRepository,
        inventory_part_repository: InventoryPartRepository,
    ):
        self.repair_order_repository = repair_order_repository
        self.inventory_part_repository = inventory_part_repository

    def execute(self) -> List[OptimizedRepairOrderResponse]:
        orders = self.repair_order_repository.get_all_pending_with_parts()
        if not orders:
            raise NoAvailableRepairOrdersException()
        
        stock = {part.id: part.stock_quantity for part in self.inventory_part_repository.get_all()}
        part_prices = {part.id: part.final_price for part in self.inventory_part_repository.get_all()}
        optimized_orders: List[OptimizedRepairOrderResponse] = []

        for order in orders:
            if order.labor_cost < 0:
                raise InvalidRepairOrderDataException(order.id, "Labor cost cannot be negative")
            if not order.parts:
                raise InvalidRepairOrderDataException(order.id, "Order has no associated parts")

            if not is_order_fulfillable(order, stock): 
                continue

            parts_total = sum(
                part_prices.get(ro_part.part_id, 0.0) * ro_part.quantity
                for ro_part in order.parts
            )
            total_cost_repair = round(order.labor_cost + parts_total, 2)

            profit = calculate_order_profit(order, self.inventory_part_repository)

            optimized_orders.append(
                OptimizedRepairOrderResponse(
                    repair_order_id=order.id,
                    customer=CustomerSimpleResponse.model_validate(order.customer),
                    vehicle=VehicleSimpleResponse.model_validate(order.vehicle),
                    total_cost_repair=total_cost_repair,
                    expected_profit=round(profit, 2)
                )
                )

            for ro_part in order.parts:
                stock[ro_part.part_id] -= ro_part.quantity

        return sorted(optimized_orders, key=lambda x: x.expected_profit, reverse=True)
    