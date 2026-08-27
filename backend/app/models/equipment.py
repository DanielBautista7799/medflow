from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Numeric, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import Enum as SqlEnum
from app.models.enums import EquipmentStatus
from .base import Base



if TYPE_CHECKING:
    from .hospital import Hospital
    from .work_order import WorkOrder

class Equipment(Base):
    __tablename__ = "equipment"

    __table_args__ = (
        CheckConstraint(
            "charge_level BETWEEN 0 and 100",
            name="charge_level_range"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True)
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[EquipmentStatus] = mapped_column(
        SqlEnum(EquipmentStatus,
                name="equipment_status",
                values_callable = lambda enum_cls:[member.value for member in enum_cls],
        )
    )
    charge_level : Mapped[Decimal]= mapped_column(Numeric(5,2))
    facility_id: Mapped[int]= mapped_column(Integer, ForeignKey("hospitals.id") )
    hospital: Mapped["Hospital"] = relationship(back_populates="equipment")
    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="equipment")
    
    LOW_CHARGE_THRESHOLD: int = 20

    def is_low_charge(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else Equipment.LOW_CHARGE_THRESHOLD
        return self.charge_level < limit
    
    def needs_maintenance(self) -> bool:
        return self.status == EquipmentStatus.MAINTENANCE
    
    def __repr__(self) -> str:
        return (
            f"Equipment(id={self.id}, serial={self.serial_number!r}, "
            f"model={self.model!r}, charge={self.charge_level}%, "
            f"status={self.status.value})"
        )