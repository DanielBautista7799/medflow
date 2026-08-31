from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models.work_order import WorkOrder
from app.schemas.work_order import WorkOrderRead, WorkOrderStatusUpdate, CoLocationDiscrepancyRead
from app.models.enums import WorkOrderPriority, WorkOrderStatus, UserRole
from app.models.equipment import Equipment
from app.models.technician import Technician
from app.models.user import User

router =APIRouter(prefix= "/work-orders", tags=["work-orders"])   

@router.get("/discrepancies", response_model=list[CoLocationDiscrepancyRead])
async def get_colocation_dependancies(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), priority: WorkOrderPriority | None = Query(
    default= None,
    description="Only return discrepancies for work orders of this priority"
)):
    statement = (select(WorkOrder.id.label("work_order_id"),
                    WorkOrder.title,
                    Equipment.facility_id.label("equipment_facility_id"),
                    Technician.facility_id.label("technician_facility_id"),
                    ).join(Technician, Technician.id == WorkOrder.technician_id )
                    .join(Equipment, Equipment.id == WorkOrder.equipment_id)
                    .where(Equipment.facility_id != Technician.facility_id)
    )
    if priority is not None:
        statement = statement.where(WorkOrder.priority == priority)
    statement = statement.order_by(WorkOrder.id)

    result = await db.execute(statement)
    return [dict(row)for row in result.mappings().all()]

    



@router.get(path="/{work_order_id}", response_model=WorkOrderRead)
async def get_work_order(work_order_id:int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user))-> WorkOrder:
        work_order = await db.get(WorkOrder, work_order_id)
        if work_order is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail = (f"work order of id {work_order_id} not found")
            )
        return work_order

@router.patch("/{work_order_id}/status", response_model=WorkOrderRead)
async def update_work_order_status(work_order_id: int, update: WorkOrderStatusUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role(UserRole.CLINICAL_ADMIN, UserRole.FIELD_TECHNICIAN)),):
    statement = (select(WorkOrder).where(WorkOrder.id == work_order_id))
    result = await db.execute(statement)
    work_order =  result.scalars().first()
    if work_order is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Work_order not found"
        )
    if update.status == WorkOrderStatus.COMPLETED:
        work_order.mark_completed()
    elif update.status == WorkOrderStatus.PENDING or update.status == WorkOrderStatus.IN_PROGRESS:
        work_order.status = update.status
    elif update.status == WorkOrderStatus.FAILED:
        work_order.mark_failed()
    await db.commit()
    await db.refresh(work_order)
    return work_order