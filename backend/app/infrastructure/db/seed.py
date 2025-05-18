import os
import uuid
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.infrastructure.db.models import Base
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.infrastructure.db.models import Customer as CustomerORM

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

def seed_database():
    session = Session(bind=engine)

    customer_repo = CustomerRepository(session)

    for _ in range(10):
        customer_data = create_fake_customer()
        customer = CustomerORM(**customer_data)
        customer_repo.add(customer)

    session.commit()
    session.close()
    print("Database populated with mocked data.")

if __name__ == "__main__":
    seed_database()
