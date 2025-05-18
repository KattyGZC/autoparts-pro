from app.infrastructure.db.models import Customer as CustomerORM
from sqlalchemy.orm import Session
from uuid import UUID
from app.domain.models import Customer
from app.infrastructure.repositories.base_repository import BaseRepository
from typing import Optional

class CustomerRepository(BaseRepository[CustomerORM]):
    def __init__(self, db: Session):
        super().__init__(db, CustomerORM)

    def add(self, customer: Customer) -> Customer:
        orm_customer = CustomerORM(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            address=customer.address,
        )
        db_obj = super().add(orm_customer)
        return Customer(
            id=db_obj.id,
            name=db_obj.name,
            email=db_obj.email,
            phone=db_obj.phone,
            address=db_obj.address,
        )

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        return super().get_by_id(customer_id)

    def get_all(self) -> list[Customer]:
        return super().get_all()

    def update(self, customer_id: UUID, updates: dict) -> Customer | None:
        return super().update(customer_id, updates)

    def delete(self, customer_id: UUID) -> bool:
        return super().delete(customer_id)

    def get_by_email(self, email: str) -> Optional[CustomerORM]:
        return self.db.query(CustomerORM).filter(CustomerORM.email == email).first()

    def get_by_phone(self, phone: str) -> Optional[CustomerORM]:
        return self.db.query(CustomerORM).filter(CustomerORM.phone == phone).first()