from app.infrastructure.db.models import Vehicle as VehicleORM
from sqlalchemy.orm import Session
from uuid import UUID
from app.domain.models import Vehicle
from app.infrastructure.repositories.base_repository import BaseRepository
from typing import Optional

class VehicleRepository(BaseRepository[VehicleORM]):
    def __init__(self, db: Session):
        super().__init__(db, VehicleORM)

    def add(self, vehicle: Vehicle) -> Vehicle:
        orm_vehicle = VehicleORM(
            id=vehicle.id,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            license_plate=vehicle.license_plate,
            color=vehicle.color,
            customer_id=vehicle.customer_id,
            is_active=vehicle.is_active,
        )
        db_obj = super().add(orm_vehicle)
        return Vehicle(
            id=db_obj.id,
            brand=db_obj.brand,
            model=db_obj.model,
            year=db_obj.year,
            license_plate=db_obj.license_plate,
            color=db_obj.color,
            customer_id=db_obj.customer_id,
            is_active=db_obj.is_active,
        )

    def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        return super().get_by_id(vehicle_id)

    def get_all(self) -> list[Vehicle]:
        return (self.db.query(self.model)
                .order_by(self.model.is_active.desc())
                .all())

    def update(self, vehicle_id: UUID, updates: dict) -> Vehicle | None:
        return super().update(vehicle_id, updates)

    def disable(self, vehicle_id: UUID) -> bool:
        return super().disable(vehicle_id)

    def get_by_license_plate(self, license_plate: str) -> Optional[VehicleORM]:
        return self.db.query(VehicleORM).filter(VehicleORM.license_plate == license_plate).first()

    def get_vehicles_by_customer_id(self, customer_id: UUID) -> list[VehicleORM]:
        return self.db.query(VehicleORM).filter(VehicleORM.customer_id == customer_id).all()
    