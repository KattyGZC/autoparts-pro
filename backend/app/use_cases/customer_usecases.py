from typing import List, Optional
from app.domain.models import Customer
from app.adapters.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerRead
)
from app.infrastructure.repositories.customer_repository import CustomerRepository
import uuid
from app.domain.exceptions import CustomerDuplicateException, CustomerNotFoundException

class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def create_customer(self, customer_data: CustomerCreate) -> CustomerRead:
        if customer_data.email and self.repository.get_by_email(customer_data.email):
            raise CustomerDuplicateException("email", customer_data.email)
        if customer_data.phone and self.repository.get_by_phone(customer_data.phone):
            raise CustomerDuplicateException("phone", customer_data.phone)
        new_customer = Customer(
            id=uuid.uuid4(),
            name=customer_data.name,
            email=customer_data.email,
            phone=customer_data.phone,
            address=customer_data.address,
            is_active=customer_data.is_active,
        )
        orm_customer = self.repository.add(new_customer)
        return CustomerRead.model_validate(orm_customer)

    def get_customer_by_id(self, customer_id: uuid.UUID) -> Optional[CustomerRead]:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(customer_id)
        return CustomerRead.model_validate(customer)

    def get_all_customers(self) -> List[CustomerRead]:
        customers = self.repository.get_all()
        return [CustomerRead.model_validate(c) for c in customers]

    def update_customer(self, customer_id: uuid.UUID, data: CustomerUpdate) -> Optional[CustomerRead]:
        updated_customer = self.repository.update(customer_id, data.model_dump(exclude_unset=True))
        if not updated_customer:
            raise CustomerNotFoundException(customer_id)
        return CustomerRead.model_validate(updated_customer)

    def disable_customer(self, customer_id: uuid.UUID) -> bool:
        return self.repository.disable(customer_id)
