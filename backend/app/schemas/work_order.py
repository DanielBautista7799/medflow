from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import WorkOrderPriority, WorkOrderStatus

class WorkOrderStatusUpdate(BaseModel):
    status: WorkOrderStatus

class WorkOrderRead(BaseModel):
    id: int
    title: str = Field(min_length = 1, max_length = 100)
    priority : WorkOrderPriority
    status: WorkOrderStatus
    equipment_id:int
    technician_id: int
    model_config = ConfigDict(from_attributes=True)

class CoLocationDiscrepancyRead(BaseModel):
    work_order_id: int
    title:str = Field(min_length = 1, max_length = 150)
    priority : WorkOrderPriority
    status: WorkOrderStatus
    equipment_facility_id:int
    technician_facility_id: int
    model_config = ConfigDict(from_attributes=True)
