from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.adapters.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleRead,
)
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.use_cases.vehicle_usecases import VehicleUseCase
from app.domain.exceptions import VehicleDuplicateException, VehicleValidationException, VehicleNotFoundException

router = APIRouter(prefix="/api/v1/vehicles", tags=["Vehicles"])

def get_vehicle_use_case(db: Session = Depends(get_db)) -> VehicleUseCase:
    repository = VehicleRepository(db)
    return VehicleUseCase(repository)

@router.post("/create", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_data: VehicleCreate,
    use_case: VehicleUseCase = Depends(get_vehicle_use_case),
):
    "Allows to create a new vehicle"
    try:
        return use_case.create_vehicle(vehicle_data)
    except VehicleDuplicateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except VehicleValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#--------------------------------------------------------------------------------------------

@router.get("/list", response_model=list[VehicleRead])
def get_all_vehicles(
    use_case: VehicleUseCase = Depends(get_vehicle_use_case),
):
    "Allows to get all vehicles"
    try:
        return use_case.get_all_vehicles()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#--------------------------------------------------------------------------------------------

@router.get("/detail/{vehicle_id}", response_model=VehicleRead)
def get_vehicle_by_id(
    vehicle_id: UUID,
    use_case: VehicleUseCase = Depends(get_vehicle_use_case),
):
    "Allows to get a vehicle by id"
    try:
        vehicle = use_case.get_vehicle_by_id(vehicle_id)
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return vehicle

#--------------------------------------------------------------------------------------------

@router.put("/update/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(
    vehicle_id: UUID,
    vehicle_data: VehicleUpdate,
    use_case: VehicleUseCase = Depends(get_vehicle_use_case),
):
    "Allows to update a vehicle by id"
    try:
        updated = use_case.update_vehicle(vehicle_id, vehicle_data)
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except VehicleDuplicateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except VehicleValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return updated

#--------------------------------------------------------------------------------------------

@router.delete("/delete/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: UUID,
    use_case: VehicleUseCase = Depends(get_vehicle_use_case),
):
    "Allows to delete a vehicle by id"
    try:
        deleted = use_case.delete_vehicle(vehicle_id)
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return deleted
