from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentRead
from app.dependencies import get_current_user, require_role, get_db
from app.models.enums import UserRole, EquipmentStatus
from app.models.user import User

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.get("", response_model=list[EquipmentRead])
async def list_equipment( max_charge: Decimal | None = Query(
    default=None,
    ge=0,
    le=100,
    description="Only return equipment below this charge percentage"
), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[Equipment]:

    statement = select(Equipment).where(Equipment.status != EquipmentStatus.OFFLINE)

    if max_charge is not None:
        statement = statement.where(Equipment.charge_level < max_charge)
    statement = statement.order_by(Equipment.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

@router.get(path="/{equipment_id}", response_model= EquipmentRead)
async def get_equipment(equipment_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Equipment:

    equipment = await db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=(f"EquipmentId = {equipment_id} not found ")
        )
    return equipment

#payload means that the user must send a response in the JSON format so ti can be stored in payload
@router.post(path="", response_model=EquipmentRead, status_code= status.HTTP_201_CREATED)
async def create_equipment(payload: EquipmentCreate,current_user: User = Depends(
    require_role(UserRole.CLINICAL_ADMIN)
), db: AsyncSession = Depends(get_db)):
    #** spreads it across the equpment argumanets .modeldump turns the pydantic obj and turns it into python
    """ same as 
    Equipment(
    serial_number=payload.serial_number,
    model=payload.model,
    status=payload.status,
    charge_level=payload.charge_level,
    facility_id=payload.facility_id
)"""
    equipment = Equipment(**payload.model_dump())
    #no need to be waited on just a stage 
    db.add(equipment)
    await db.commit()
    #update so it appears
    await db.refresh(equipment)

    return equipment


