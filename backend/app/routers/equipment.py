from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.equipment import Equipment
from app.models.enums import EquipmentStatus
from app.schemas.equipment import EquipmentCreate, EquipmentRead

router = APIRouter(prefix="/equipment", tags=["equipement"])

@router.get("", response_model=list[EquipmentRead])
async def list_equipment( max_charge: Decimal | None = Query(
    default=None,
    ge=0,
    le=100,
    description="Only return equipment below this charge percentage"
), db: AsyncSession = Depends(get_db)) -> list[Equipment]:

    statement = select(Equipment).where(Equipment.status != EquipmentStatus.OFFLINE)

    if max_charge is not None:
        statement = statement.where(Equipment.charge_level < max_charge)
    statement = statement.order_by(Equipment.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

@router.get(path="/{equipment_id}", response_model= EquipmentRead)
async def get_equipment(equipment_id: int, db: AsyncSession = Depends(get_db)) -> Equipment:

    equipment = await db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=(f"EquipmentId = {equipment_id} not found ")
        )
    return equipment
