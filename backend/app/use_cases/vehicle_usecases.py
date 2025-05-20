from typing import List, Optional
from app.domain.models import Vehicle
from app.adapters.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleRead
)
from app.infrastructure.repositories.vehicle_repository import VehicleRepository
from app.infrastructure.repositories.customer_repository import CustomerRepository
import uuid
from app.domain.exceptions import VehicleDuplicateException, VehicleNotFoundException, VehicleValidationException, CustomerNotFoundException

class VehicleUseCase:
    def __init__(self, repository: VehicleRepository, customer_repo: CustomerRepository):
        self.repository = repository
        self.customer_repo = customer_repo

    def create_vehicle(self, vehicle_data: VehicleCreate) -> VehicleRead:
        if vehicle_data.license_plate and self.repository.get_by_license_plate(vehicle_data.license_plate):
            raise VehicleDuplicateException("license_plate", vehicle_data.license_plate)
        if not vehicle_data.customer_id:
            raise VehicleValidationException("Customer ID is required.")
        if not self.customer_repo.get_by_id(vehicle_data.customer_id):
            raise CustomerNotFoundException(vehicle_data.customer_id)
    
        new_vehicle = Vehicle(
            id=uuid.uuid4(),
            brand=vehicle_data.brand,
            model=vehicle_data.model,
            year=vehicle_data.year,
            license_plate=vehicle_data.license_plate,
            color=vehicle_data.color,
            customer_id=vehicle_data.customer_id,
            is_active=True,
        )
        orm_vehicle = self.repository.add(new_vehicle)
        return VehicleRead.model_validate(orm_vehicle)

    def get_vehicle_by_id(self, vehicle_id: uuid.UUID) -> Optional[VehicleRead]:
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException(vehicle_id)
        return VehicleRead.model_validate(vehicle)

    def get_all_vehicles(self) -> List[VehicleRead]:
        vehicles = self.repository.get_all()
        return [VehicleRead.model_validate(v) for v in vehicles]

    def update_vehicle(self, vehicle_id: uuid.UUID, data: VehicleUpdate) -> Optional[VehicleRead]:
        if not data.customer_id:
            raise VehicleValidationException("Customer ID is required.")
        if not self.customer_repo.get_by_id(data.customer_id):
            raise CustomerNotFoundException(data.customer_id)
        updated_vehicle = self.repository.update(vehicle_id, data.model_dump(exclude_unset=True))
        if not updated_vehicle:
            raise VehicleNotFoundException(vehicle_id)
        return VehicleRead.model_validate(updated_vehicle)

    def disable_vehicle(self, vehicle_id: uuid.UUID) -> bool:
        return self.repository.disable(vehicle_id)
