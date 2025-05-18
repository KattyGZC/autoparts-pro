import os
import uuid
import random
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.infrastructure.db.models import Base
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.db.models import Customer as CustomerORM, Vehicle as VehicleORM

fake = Faker()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/postgres")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

def create_fake_customer():
    return {
        "id": uuid.uuid4(),
        "name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.unique.phone_number(),
        "address": fake.address()
    }

def create_fake_vehicle(customer_id):
    colors = ["red", "blue", "green", "yellow", "black", "white", "gray", "silver", "gold", "bronze"]
    return {
        "id": uuid.uuid4(),
        "customer_id": customer_id,
        "license_plate": fake.unique.license_plate(),
        "model": fake.word(),
        "brand": fake.company(),
        "color": random.choice(colors),
        "year": fake.year()
    }

def seed_database():
    session = Session(bind=engine)

    customer_repo = CustomerRepository(session)
    vehicle_repo = VehicleRepository(session)

    for _ in range(10):
        customer_data = create_fake_customer()
        customer = CustomerORM(**customer_data)
        customer_repo.add(customer)

        for _ in range(2):
            vehicle_data = create_fake_vehicle(customer.id)
            vehicle = VehicleORM(**vehicle_data)
            vehicle_repo.add(vehicle)

    session.commit()
    session.close()
    print("Database populated with mocked data.")

if __name__ == "__main__":
    seed_database()
