from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.adapters.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerRead,
)
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.use_cases.customer_usecases import CustomerUseCase
from app.domain.exceptions import CustomerDuplicateException, CustomerValidationException, CustomerNotFoundException

router = APIRouter(prefix="/api/v1/customers", tags=["Customers"])

def get_customer_use_case(db: Session = Depends(get_db)) -> CustomerUseCase:
    repository = CustomerRepository(db)
    return CustomerUseCase(repository)

@router.post("/create", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_data: CustomerCreate,
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    "Allows to create a new customer"
    try:
        return use_case.create_customer(customer_data)
    except CustomerDuplicateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except CustomerValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/list", response_model=list[CustomerRead])
def get_all_customers(
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    "Allows to get all customers"
    try:
        return use_case.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/detail/{customer_id}", response_model=CustomerRead)
def get_customer_by_id(
    customer_id: UUID,
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    "Allows to get a customer by id"
    try:
        customer = use_case.get_customer_by_id(customer_id)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return customer

#--------------------------------------------------------------------------------------------

@router.put("/update/{customer_id}", response_model=CustomerRead)
def update_customer(
    customer_id: UUID,
    customer_data: CustomerUpdate,
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    "Allows to update a customer by id"
    try:
        updated = use_case.update_customer(customer_id, customer_data)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CustomerDuplicateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except CustomerValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return updated

#--------------------------------------------------------------------------------------------

@router.delete("/delete/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: UUID,
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    "Allows to delete a customer by id"
    try:
        deleted = use_case.delete_customer(customer_id)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return deleted
