from typing import Optional
from uuid import UUID
from app.adapters.schemas.base import BaseSchema
from pydantic.networks import EmailStr
from pydantic import constr

class CustomerBase(BaseSchema):
    name: constr(min_length=2, max_length=100, strip_whitespace=True)
    email: Optional[EmailStr] = None
    phone: Optional[constr(min_length=7, max_length=15)] = None
    address: Optional[constr(min_length=5, max_length=150, strip_whitespace=True)] = None
    is_active: bool = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: UUID
    is_active: bool
