from app.domain.models import RepairOrder
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository


def calculate_order_profit(order: RepairOrder, inventory_repo: InventoryPartRepository) -> float:
    profit = 0.0
    for ro_part in order.parts:
        part = inventory_repo.get_by_id(ro_part.part_id)
        unit_profit = part.final_price - part.cost
        profit += unit_profit * ro_part.quantity
    return profit + order.labor_cost
