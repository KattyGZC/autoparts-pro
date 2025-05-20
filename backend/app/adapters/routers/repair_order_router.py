from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from uuid import UUID
from sqlalchemy.orm import Session
from app.adapters.schemas.repair_order import (
    RepairOrderCreate,
    RepairOrderUpdate,
    RepairOrderRead
)
from app.adapters.schemas.inventory_part import PartDetailByInventoryPart
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.use_cases.repair_order_usecases import RepairOrderUseCase
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
from app.domain.exceptions import RepairOrderValidationException, RepairOrderNotFoundException
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.infrastructure.repositories.repair_order_part_repository import RepairOrderPartRepository
from app.use_cases.repair_order_part_usecases import RepairOrderPartUseCase

router = APIRouter(prefix="/api/v1/repair_orders", tags=["Repair Orders"])

def get_repair_order_use_case(db: Session = Depends(get_db)) -> RepairOrderUseCase:
    vehicle_repo= VehicleRepository(db)
    customer_repo= CustomerRepository(db)
    repository = RepairOrderRepository(db)
    repair_order_part_repo = RepairOrderPartRepository(db)
    part_repo = InventoryPartRepository(db)
    repair_order_part_usecase = RepairOrderPartUseCase(repair_order_part_repo, repository, part_repo)
    return RepairOrderUseCase(repository, vehicle_repo, customer_repo, part_repo, repair_order_part_usecase, repair_order_part_repo)

@router.post("/create", response_model=RepairOrderRead, status_code=status.HTTP_201_CREATED)
def create_repair_order(
    repair_order_data: RepairOrderCreate,
    use_case: RepairOrderUseCase = Depends(get_repair_order_use_case),
):
    "Allows to create a new part"
    try:
        return use_case.create_repair_order(repair_order_data)
    except RepairOrderValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/list", response_model=list[RepairOrderRead])
def get_all_repair_orders(
    use_case: RepairOrderUseCase = Depends(get_repair_order_use_case),
):
    "Allows to get all repair orders"
    try:
        return use_case.get_all_repair_orders()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#--------------------------------------------------------------------------------------------

@router.get("/detail/{repair_order_id}", response_model=RepairOrderRead)
def get_repair_order_by_id(
    repair_order_id: UUID,
    use_case: RepairOrderUseCase = Depends(get_repair_order_use_case),
):
    "Allows to get a repair order by id"
    try:
        repair_order = use_case.get_repair_order_by_id(repair_order_id)
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return repair_order

#--------------------------------------------------------------------------------------------

@router.put("/update/{repair_order_id}", response_model=RepairOrderRead)
def update_repair_order(
    repair_order_id: UUID,
    repair_order_data: RepairOrderUpdate,
    use_case: RepairOrderUseCase = Depends(get_repair_order_use_case),
):
    "Allows to update a part by id"
    try:
        updated = use_case.update_repair_order(repair_order_id, repair_order_data)
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RepairOrderValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
    return updated

#--------------------------------------------------------------------------------------------

@router.get("/vehicle/{vehicle_id}", response_model=list[RepairOrderRead])
def get_repair_orders_by_vehicle_id(
    vehicle_id: UUID,
    use_case: RepairOrderUseCase = Depends(get_repair_order_use_case),
):
    "Allows to get a repair order by vehicle id"
    try:
        repair_orders = use_case.get_repair_orders_by_vehicle_id(vehicle_id)
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return repair_orders

#--------------------------------------------------------------------------------------------

@router.get("/{repair_order_id}/parts-used", response_model=list[PartDetailByInventoryPart])
def get_parts_used_in_order(
    repair_order_id: UUID,
    use_case: RepairOrderUseCase = Depends(get_repair_order_use_case),
):
    "Allows to get the parts used in a repair order"
    try:
        parts = use_case.get_parts_used_in_order(repair_order_id)
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return parts
