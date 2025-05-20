import os
import uuid
import random
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.infrastructure.db.models import Base
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.repair_order_part_repository import RepairOrderPartRepository
from app.infrastructure.db.models import (Customer as CustomerORM, Vehicle as VehicleORM, InventoryPart as InventoryPartORM,
                                          RepairOrder as RepairOrderORM, RepairOrderPart as RepairOrderPartORM)

fake = Faker()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/postgres")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)


def create_fake_customer():
    return {
        "id": uuid.uuid4(),
        "name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.unique.numerify(text='###########'),
        "address": fake.address()
    }


def create_fake_vehicle(customer_id):
    colors = ["red", "blue", "green", "yellow", "black",
              "white", "gray", "silver", "gold", "bronze"]
    brands = ["Toyota", "Honda", "Ford", "Chevrolet", "Dodge",
              "BMW", "Audi", "Mercedes", "Volkswagen", "Jaguar"]
    return {
        "id": uuid.uuid4(),
        "customer_id": customer_id,
        "license_plate": fake.unique.license_plate(),
        "model": fake.word(),
        "brand": random.choice(brands),
        "color": random.choice(colors),
        "year": random.randint(1980, 2024)
    }


def create_fake_inventory_part():
    names = [
        "Tires",
        "Engine Oil",
        "Oil Filter",
        "Air Filter",
        "Fuel Filter",
        "Brake Pads",
        "Brake Rotors",
        "Brake Fluid",
        "Spark Plugs",
        "Ignition Coils",
        "Battery",
        "Windshield Wiper Blades",
        "Headlight Bulbs",
        "Taillight Bulbs",
        "Fuses",
        "Belts (Serpentine, Timing)",
        "Hoses (Radiator, Heater)",
        "Radiator",
        "Water Pump",
        "Thermostat",
        "Shock Absorbers",
        "Struts",
        "Suspension Bushings",
        "Ball Joints",
        "Tie Rod Ends",
        "Wheel Bearings",
        "Clutch (if manual)",
        "Transmission Fluid",
        "Differential Fluid",
        "Power Steering Fluid",
        "Coolant",
        "Exhaust System Components (Muffler, Catalytic Converter, Pipes)",
        "Oxygen Sensors",
        "Cabin Air Filter",
        "Floor Mats",
        "Seat Covers",
        "Steering Wheel Cover"
    ]
    return {
        "id": uuid.uuid4(),
        "name": random.choice(names),
        "description": fake.text(),
        "cost": fake.pyfloat(left_digits=4, right_digits=2, positive=True),
        "stock_quantity": fake.pyint(min_value=0, max_value=100),
        "is_active": True
    }


def create_fake_repair_order(vehicle_id, customer_id):
    return {
        "id": uuid.uuid4(),
        "vehicle_id": vehicle_id,
        "customer_id": customer_id,
        "status": random.choice(["pending", "in_progress", "completed", "cancelled"]),
        "labor_cost": fake.pyfloat(left_digits=4, right_digits=2, positive=True),
        "date_in": fake.date_time(),
        "date_expected_out": fake.date_time(),
        "date_out": None,
        "is_active": True
    }


def create_fake_repair_order_part(repair_order_id, inventory_part_id):
    return {
        "id": uuid.uuid4(),
        "repair_order_id": repair_order_id,
        "part_id": inventory_part_id,
        "quantity": fake.pyint(min_value=1, max_value=10),
        "is_active": True
    }


def seed_database():
    session = Session(bind=engine)

    customer_repo = CustomerRepository(session)
    vehicle_repo = VehicleRepository(session)
    inventory_part_repo = InventoryPartRepository(session)
    repair_order_repo = RepairOrderRepository(session)
    repair_order_part_repo = RepairOrderPartRepository(session)

    for _ in range(10):
        customer_data = create_fake_customer()
        customer = CustomerORM(**customer_data)
        customer_repo.add(customer)

        for _ in range(2):
            vehicle_data = create_fake_vehicle(customer.id)
            vehicle = VehicleORM(**vehicle_data)
            vehicle_repo.add(vehicle)

            for _ in range(2):
                inventory_part_data = create_fake_inventory_part()
                inventory_part = InventoryPartORM(**inventory_part_data)
                inventory_part_repo.add(inventory_part)

                repair_order_data = create_fake_repair_order(vehicle.id, customer.id)
                repair_order = RepairOrderORM(**repair_order_data)
                repair_order_repo.add(repair_order)

                repair_order_part_data = create_fake_repair_order_part(
                    repair_order.id, inventory_part.id)
                repair_order_part = RepairOrderPartORM(
                    **repair_order_part_data)
                repair_order_part_repo.add(repair_order_part)

    session.commit()
    session.close()
    print("Database populated with mocked data.")


if __name__ == "__main__":
    seed_database()
