from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .work_order import WorkOrder

class ServiceReport(Base):
    __tablename__ = "service_reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    work_order_id : Mapped[int] = mapped_column(Integer, ForeignKey("work_orders.id"))
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str|None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    work_order: Mapped["WorkOrder"] = relationship(back_populates="service_reports")

    def __repr__(self) ->  str:
        return (f"ServiceReport(id={self.id}, work_order_id={self.work_order_id}, file_url= {self.file_url}, notes= {self.notes}, createdAt = {self.created_at})")
