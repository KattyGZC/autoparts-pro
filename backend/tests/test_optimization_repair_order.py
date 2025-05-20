import pytest
from uuid import uuid4
from app.infrastructure.db.models import (RepairOrder as RepairOrderORM, 
                                        RepairOrderPart as RepairOrderPartORM, 
                                        InventoryPart as InventoryPartORM, 
                                        Vehicle as VehicleORM, 
                                        Customer as CustomerORM)
from app.use_cases.repair_order_optimization.calculate_order_profit import calculate_order_profit
from app.use_cases.repair_order_optimization.select_orders_by_profit import SelectRepairOrdersByProfitUseCase
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.domain.exceptions import NoAvailableRepairOrdersException

def test_calculate_order_profit_simple(db):
    """Test basic profit calculation for a repair order."""
    # Create required entities
    customer = CustomerORM(id=uuid4(), name="John Doe", email="john.doe@example.com", address="123 Main St", phone="123-456-7890")
    license_plate = f"ABC {str(uuid4())[:4]}"
    vehicle = VehicleORM(id=uuid4(), license_plate=license_plate, color="red", customer_id=customer.id, brand="Toyota", model="Corolla", year=2020, is_active=True)
    db.add_all([customer, vehicle])
    db.commit()

    # Create part and repair order
    part = InventoryPartORM(id=uuid4(), name="Filtro", description="Filtro de aire", stock_quantity=5, cost=20.0, final_price=50.0, is_active=True)
    db.add(part)
    db.commit()
    db.refresh(part)

    ro_part = RepairOrderPartORM(part_id=part.id, quantity=2)
    repair_order = RepairOrderORM(
        id=uuid4(), 
        labor_cost=30.0, 
        parts=[ro_part], 
        status="pending", 
        is_active=True,
        vehicle_id=vehicle.id,
        customer_id=customer.id
    )
    db.add(repair_order)
    db.commit()
    db.refresh(repair_order)

    repo = InventoryPartRepository(db)
    profit = calculate_order_profit(repair_order, repo)
    assert profit == 90.0  # 2 * (50 - 20) + 30 = 90

def test_select_orders_by_profit_returns_sorted_list(db):
    """Test that orders are returned sorted by profit."""
    # Clean up any existing orders
    db.query(RepairOrderPartORM).delete()
    db.query(RepairOrderORM).delete()
    db.commit()

    # Create customer and vehicle
    customer = CustomerORM(id=uuid4(), name="John Doe", email="john.doe@example.com", address="123 Main St", phone="123-456-7890")
    license_plate = f"ABC {str(uuid4())[:4]}"
    vehicle = VehicleORM(id=uuid4(), license_plate=license_plate, color="red", customer_id=customer.id, brand="Toyota", model="Corolla", year=2020, is_active=True)
    db.add_all([customer, vehicle])
    db.commit()

    # Create parts
    part1 = InventoryPartORM(id=uuid4(), name="Filtro", description="Filtro de aire", stock_quantity=5, cost=20.0, final_price=50.0, is_active=True)
    part2 = InventoryPartORM(id=uuid4(), name="Aceite", description="Aceite de motor", stock_quantity=10, cost=20.0, final_price=60.0, is_active=True)
    db.add_all([part1, part2])
    db.commit()

    # Create orders with different profits
    orders = [
        # First order with higher profit (2 filtros)
        {
            "repair_order": RepairOrderORM(
                id=uuid4(),
                customer_id=customer.id,
                vehicle_id=vehicle.id,
                labor_cost=50.0,
                status="pending",
                is_active=True
            ),
            "part": part1,
            "quantity": 2,
            "expected_profit": 110.0  # 2 * (50 - 20) + 50 = 110
        },
        # Second order with lower profit (1 aceite)
        {
            "repair_order": RepairOrderORM(
                id=uuid4(),
                customer_id=customer.id,
                vehicle_id=vehicle.id,
                labor_cost=20.0,
                status="pending",
                is_active=True
            ),
            "part": part2,
            "quantity": 1,
            "expected_profit": 60.0  # (60 - 20) + 20 = 60
        }
    ]

    # Add orders and their parts to the database
    for order_data in orders:
        repair_order = order_data["repair_order"]
        part = order_data["part"]
        quantity = order_data["quantity"]
        
        ro_part = RepairOrderPartORM(repair_order_id=repair_order.id, part_id=part.id, quantity=quantity)
        db.add_all([repair_order, ro_part])
        db.commit()

    # Execute use case
    use_case = SelectRepairOrdersByProfitUseCase(
        repair_order_repository=RepairOrderRepository(db),
        inventory_part_repository=InventoryPartRepository(db)
    )

    result = use_case.execute()
    
    # Verify that all orders are sorted by profit (descending)
    for i in range(len(result) - 1):
        assert result[i].expected_profit >= result[i + 1].expected_profit
    
    # Verify that the first order has the highest profit
    assert result[0].expected_profit == 110.0
    # Verify that the last order has the lowest profit
    assert result[-1].expected_profit == 60.0



def test_no_pending_orders_raises_exception(db):
    """Test that NoAvailableRepairOrdersException is raised when no pending orders exist."""
    db.query(RepairOrderORM).delete()
    db.commit()

    use_case = SelectRepairOrdersByProfitUseCase(
        repair_order_repository=RepairOrderRepository(db),
        inventory_part_repository=InventoryPartRepository(db)
    )

    with pytest.raises(NoAvailableRepairOrdersException):
        use_case.execute()

def test_no_orders_fulfilled_due_to_stock(db):
    """Test that orders are not fulfilled when there's not enough stock."""
    db.query(RepairOrderPartORM).delete()
    db.query(RepairOrderORM).delete()
    db.query(InventoryPartORM).delete()
    db.commit()

    part = InventoryPartORM(id=uuid4(), name="Filtro", stock_quantity=0, cost=10.0, final_price=40.0, is_active=True)
    db.add(part)
    db.commit()

    customer = CustomerORM(id=uuid4(), name="John Doe", email="john.doe@example.com", address="123 Main St", phone="123-456-7890")
    license_plate = f"ABC {str(uuid4())[:4]}"
    vehicle = VehicleORM(id=uuid4(), license_plate=license_plate, color="red", customer_id=customer.id, brand="Toyota", model="Corolla", year=2020, is_active=True)
    db.add_all([customer, vehicle])
    db.commit()

    ro = RepairOrderORM(
        id=uuid4(), customer_id=customer.id, vehicle_id=vehicle.id,
        labor_cost=50.0, status="pending", is_active=True
    )
    ro_part = RepairOrderPartORM(repair_order_id=ro.id, part_id=part.id, quantity=1)
    db.add_all([ro, ro_part])
    db.commit()

    use_case = SelectRepairOrdersByProfitUseCase(
        repair_order_repository=RepairOrderRepository(db),
        inventory_part_repository=InventoryPartRepository(db)
    )

    result = use_case.execute()
    assert result == []
