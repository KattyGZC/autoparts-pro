from app.adapters.schemas.repair_order_optimization import OptimizedRepairOrderResponse
from fastapi import APIRouter, Depends, HTTPException, status
from app.use_cases.repair_order_optimization.select_orders_by_profit import SelectRepairOrdersByProfitUseCase
from app.infrastructure.repositories.repair_order_repository import RepairOrderRepository
from app.infrastructure.repositories.inventory_part_repository import InventoryPartRepository
from app.infrastructure.db.session import get_db
from sqlalchemy.orm import Session
from app.domain.exceptions import NoAvailableRepairOrdersException, InvalidRepairOrderDataException

router = APIRouter(prefix="/api/v1/repair_order_optimization", tags=["Repair Order Optimization"])

def get_repair_order_use_case(db: Session = Depends(get_db)) -> SelectRepairOrdersByProfitUseCase:
    repair_order_repo = RepairOrderRepository(db)
    inventory_part_repo = InventoryPartRepository(db)
    return SelectRepairOrdersByProfitUseCase(repair_order_repo, inventory_part_repo)

@router.get("/list", response_model=list[OptimizedRepairOrderResponse])
def get_optimized_orders(
    use_case: SelectRepairOrdersByProfitUseCase = Depends(get_repair_order_use_case),
):
    "Allows to get all optimized repair orders"
    try:
        return use_case.execute()
    except NoAvailableRepairOrdersException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidRepairOrderDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        