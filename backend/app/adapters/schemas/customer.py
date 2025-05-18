from typing import Optional
from uuid import UUID
from app.adapters.schemas.base import BaseSchema
from pydantic.networks import EmailStr

class CustomerBase(BaseSchema):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: UUID
