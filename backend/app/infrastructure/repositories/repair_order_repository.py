from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.infrastructure.db.models import RepairOrder as RepairOrderORM
from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.models import RepairOrder
from sqlalchemy.orm import joinedload

class RepairOrderRepository(BaseRepository[RepairOrderORM]):
    def __init__(self, db: Session):
        super().__init__(db, RepairOrderORM)

    def get_by_id(self, id: UUID) -> Optional[RepairOrderORM]:
        return super().get_by_id(id)

    def get_all(self) -> list[RepairOrderORM]:
        return super().get_all()

    def add(self, repair_order: RepairOrderORM) -> RepairOrderORM:
        orm_repair_order = RepairOrderORM(
            id=repair_order.id,
            vehicle_id=repair_order.vehicle_id,
            customer_id=repair_order.customer_id,
            is_active=repair_order.is_active,
            status=repair_order.status,
            labor_cost=repair_order.labor_cost,
            date_in=repair_order.date_in,
            date_expected_out=repair_order.date_expected_out,
            date_out=repair_order.date_out,
            total_cost_repair=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db_obj = super().add(orm_repair_order)
        return RepairOrder(
            id=db_obj.id,
            vehicle_id=db_obj.vehicle_id,
            customer_id=db_obj.customer_id,
            is_active=db_obj.is_active,
            status=db_obj.status,
            labor_cost=db_obj.labor_cost,
            date_in=db_obj.date_in,
            date_expected_out=db_obj.date_expected_out,
            date_out=db_obj.date_out,
            total_cost_repair=db_obj.total_cost_repair,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )

    def update(self, id: UUID, updates: dict) -> RepairOrder | None:
        return super().update(id, updates)

    def get_by_vehicle_id(self, vehicle_id: UUID) -> list[RepairOrderORM]:
        return self.db.query(RepairOrderORM).filter(RepairOrderORM.vehicle_id == vehicle_id).all()
    
    def get_all_pending_with_parts(self) -> list[RepairOrderORM]:
        return (
            self.db.query(RepairOrderORM)
            .filter(RepairOrderORM.state == "pending", RepairOrderORM.is_active == True)
            .options(joinedload(RepairOrderORM.repair_order_parts))
            .all()
        )