from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as EnumSql
from app.models.enums import WorkOrderPriority, WorkOrderStatus
from .base import Base

if TYPE_CHECKING:
    from .equipment import Equipment
    from .service_report import ServiceReport
    from .technician import Technician

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    priority: Mapped[WorkOrderPriority] = mapped_column(
        EnumSql(
            WorkOrderPriority,
            name = "work_order_priority",
            values_callable = lambda enums_cls:[member.value for member in enums_cls]
        )
    )
    status: Mapped[WorkOrderStatus] = mapped_column(
        EnumSql(
            WorkOrderStatus,
            name="work_order_status",
            values_callable = lambda enums_cls:[member.value for member in enums_cls]
        )
    )
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipment.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))

    equipment: Mapped["Equipment"] = relationship(back_populates="work_orders")
    service_reports: Mapped[list["ServiceReport"]] = relationship(back_populates="work_order")
    technician: Mapped["Technician"] = relationship(back_populates="work_orders")

    def mark_completed(self) -> None:
        self.status = WorkOrderStatus.COMPLETED

    def mark_failed(self) -> None:
        self.status = WorkOrderStatus.FAILED

    

    def __repr__(self) -> str:
        return (f"WorkOrderId = '{self.id}', Title = '{self.title}', Priority = '{self.priority.value}', status = '{self.status.value}'")
