from app.domain.models import RepairOrder

def is_order_fulfillable(order: RepairOrder, current_stock: dict) -> bool:
    for ro_part in order.parts:
        part_id = ro_part.part_id
        if current_stock.get(part_id, 0) < ro_part.quantity:
            return False
    return True