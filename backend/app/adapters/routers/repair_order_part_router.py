from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from uuid import UUID
from sqlalchemy.orm import Session
from app.adapters.schemas.repair_order_part import (
    RepairOrderPartCreate,
    RepairOrderPartUpdate,
    RepairOrderPartRead,
)
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.repair_order_part_repository import RepairOrderPartRepository  
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.use_cases.repair_order_part_usecases import RepairOrderPartUseCase
from app.domain.exceptions import RepairOrderPartValidationException, RepairOrderNotFoundException, InventoryPartNotFoundException

router = APIRouter(prefix="/api/v1/repair_order_parts", tags=["Repair Order Parts"])

def get_repair_order_part_use_case(db: Session = Depends(get_db)) -> RepairOrderPartUseCase:
    repository = RepairOrderPartRepository(db)
    repair_order_repository = RepairOrderRepository(db)
    part_repository = InventoryPartRepository(db)
    return RepairOrderPartUseCase(repository, repair_order_repository, part_repository)

@router.post("/create", response_model=RepairOrderPartRead, status_code=status.HTTP_201_CREATED)
def create_repair_order_part(
    repair_order_data: RepairOrderPartCreate,
    use_case: RepairOrderPartUseCase = Depends(get_repair_order_part_use_case),
):
    "Allows to create a new repair order part"
    try:
        return use_case.create_repair_order_part(repair_order_data)
    except RepairOrderPartValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InventoryPartNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/list", response_model=list[RepairOrderPartRead])
def get_all_repair_order_parts(
    use_case: RepairOrderPartUseCase = Depends(get_repair_order_part_use_case),
):
    "Allows to get all repair order parts"
    try:
        return use_case.get_all_repair_order_parts()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#--------------------------------------------------------------------------------------------

@router.get("/detail/{repair_order_id}", response_model=RepairOrderPartRead)
def get_repair_order_part_by_id(
    repair_order_id: UUID,
    use_case: RepairOrderPartUseCase = Depends(get_repair_order_part_use_case),
):
    "Allows to get a repair order part by id"
    try:
        repair_order = use_case.get_repair_order_part_by_id(repair_order_id)
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return repair_order

#--------------------------------------------------------------------------------------------

@router.put("/update/{repair_order_id}", response_model=RepairOrderPartRead)
def update_repair_order_part(
    repair_order_id: UUID,
    repair_order_data: RepairOrderPartUpdate,
    use_case: RepairOrderPartUseCase = Depends(get_repair_order_part_use_case),
):
    "Allows to update a repair order part by id"
    try:
        updated = use_case.update_repair_order_part(repair_order_id, repair_order_data)
    except RepairOrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RepairOrderPartValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return updated
