"""
MedFlow Command Center
Business Question #4 - Hospital Maintenance Flags.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.equipment import Equipment
from app.models.enums import EquipmentStatus, WorkOrderStatus
from app.models.hospital import Hospital
from app.models.user import User
from app.schemas.hospital import (
    MaintenanceFlag,
    TechnicianActiveWorkOrders,
    ReportingLineResult,
)
from app.models.technician import Technician
from app.models.work_order import WorkOrder


router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.get("/maintenance-flags", response_model=list[MaintenanceFlag])
async def maintenance_flags(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    maintenance_count = func.sum(
        case(
            (Equipment.status == EquipmentStatus.MAINTENANCE, 1),
            else_=0,
        )
    )

    total_equipment = func.count(Equipment.id)

    maintenance_pct = (
        maintenance_count * 100.0 / total_equipment
    )

    statement = (
        select(
            Hospital.id.label("hospital_id"),
            Hospital.name.label("hospital_name"),
            total_equipment.label("total_equipment"),
            maintenance_count.label("maintenance_count"),
            maintenance_pct.label("maintenance_percentage"),
        )
        .join(
            Equipment,
            Equipment.facility_id == Hospital.id,
        )
        .group_by(
            Hospital.id,
            Hospital.name,
        )
        .having(maintenance_pct > 30)
        .order_by(Hospital.id)
    )

    result = await db.execute(statement)

    return [
        dict(row)
        for row in result.mappings().all()
    ]

@router.get("/reporting-lines", response_model=ReportingLineResult)
async def reporting_lines(
    supervisor_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    statement = (
        select(
            Technician.id.label("technician_id"),
            Technician.name.label("technician_name"),
            func.count(WorkOrder.id).label("active_work_order_count"),
        )
        .join(
            Hospital,
            Hospital.id == Technician.facility_id,
        )
        .join(
            WorkOrder,
            WorkOrder.technician_id == Technician.id,
        )
        .where(
            Hospital.supervisor_id == supervisor_id,
            WorkOrder.status.in_(
                [
                    WorkOrderStatus.PENDING,
                    WorkOrderStatus.IN_PROGRESS,
                ]
            ),
        )
        .group_by(
            Technician.id,
            Technician.name,
        )
        .order_by(Technician.id)
    )

    result = await db.execute(statement)

    technicians = [
        TechnicianActiveWorkOrders(**row)
        for row in result.mappings().all()
    ]

    return ReportingLineResult(
        supervisor_id=supervisor_id,
        technician_count=len(technicians),
        technicians=technicians,
    )