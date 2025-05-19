from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from uuid import UUID
from sqlalchemy.orm import Session
from app.adapters.schemas.inventory_part import (
    InventoryPartCreate,
    InventoryPartUpdate,
    InventoryPartRead,
)
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.use_cases.inventory_part_usecases import InventoryPartUseCase
from app.domain.exceptions import InventoryPartDuplicateException, InventoryPartValidationException, InventoryPartNotFoundException

router = APIRouter(prefix="/api/v1/inventory_parts", tags=["Inventory Parts"])

def get_inventory_part_use_case(db: Session = Depends(get_db)) -> InventoryPartUseCase:
    repository = InventoryPartRepository(db)
    return InventoryPartUseCase(repository)

@router.post("/create", response_model=InventoryPartRead, status_code=status.HTTP_201_CREATED)
def create_inventory_part(
    inventory_part_data: InventoryPartCreate,
    use_case: InventoryPartUseCase = Depends(get_inventory_part_use_case),
):
    "Allows to create a new part"
    try:
        return use_case.create_inventory_part(inventory_part_data)
    except InventoryPartDuplicateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InventoryPartValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/list", response_model=list[InventoryPartRead])
def get_all_inventory_parts(
    use_case: InventoryPartUseCase = Depends(get_inventory_part_use_case),
):
    "Allows to get all parts"
    try:
        return use_case.get_all_inventory_parts()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/detail/{inventory_part_id}", response_model=InventoryPartRead)
def get_inventory_part_by_id(
    inventory_part_id: UUID,
    use_case: InventoryPartUseCase = Depends(get_inventory_part_use_case),
):
    "Allows to get a part by id"
    try:
        inventory_part = use_case.get_inventory_part_by_id(inventory_part_id)
    except InventoryPartNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return inventory_part

#--------------------------------------------------------------------------------------------

@router.put("/update/{inventory_part_id}", response_model=InventoryPartRead)
def update_inventory_part(
    inventory_part_id: UUID,
    inventory_part_data: InventoryPartUpdate,
    use_case: InventoryPartUseCase = Depends(get_inventory_part_use_case),
):
    "Allows to update a part by id"
    try:
        updated = use_case.update_inventory_part(inventory_part_id, inventory_part_data)
    except InventoryPartNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InventoryPartDuplicateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InventoryPartValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return updated

#--------------------------------------------------------------------------------------------

@router.patch("/disable/{inventory_part_id}", status_code=status.HTTP_200_OK)
def disable_inventory_part(
    inventory_part_id: UUID,
    use_case: InventoryPartUseCase = Depends(get_inventory_part_use_case),
):
    "Allows to disable (soft delete) a part by id"
    try:
        use_case.disable_inventory_part(inventory_part_id)
    except InventoryPartNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return JSONResponse(status_code=200, content={"detail": "Part deactivated successfully"})
