"""
MedFlow Command Center
Day 10 - RBAC tests for PATCH /work-orders/{work_order_id}/status.
"""

import pytest_asyncio

from app.models import (
    Equipment,
    EquipmentStatus,
    Technician,
    WorkOrder,
    WorkOrderPriority,
    WorkOrderStatus,
)
from tests.conftest import auth_header


# Creates the equipment + technician + work order needed for these tests.
@pytest_asyncio.fixture
async def seeded_work_order(
    db_session,
    seeded_hospital,
):
    equipment = Equipment(
        serial_number="MX-0001",
        model="Test-Device",
        status=EquipmentStatus.AVAILABLE,
        charge_level=75,
        facility_id=seeded_hospital.id,
    )

    technician = Technician(
        name="Test Technician",
        facility_id=seeded_hospital.id,
    )

    db_session.add_all([equipment, technician])
    await db_session.commit()

    await db_session.refresh(equipment)
    await db_session.refresh(technician)

    work_order = WorkOrder(
        title="Test Work Order",
        priority=WorkOrderPriority.LOW,
        status=WorkOrderStatus.PENDING,
        equipment_id=equipment.id,
        technician_id=technician.id,
    )

    db_session.add(work_order)
    await db_session.commit()
    await db_session.refresh(work_order)

    return work_order


# Clinical Admin should be able to update work-order status.
async def test_clinical_admin_can_update_status(
    client,
    seeded_users,
    seeded_work_order,
):
    response = await client.patch(
        f"/work-orders/{seeded_work_order.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


# Field Technician should also be able to update work-order status.
async def test_field_technician_can_update_status(
    client,
    seeded_users,
    seeded_work_order,
):
    response = await client.patch(
        f"/work-orders/{seeded_work_order.id}/status",
        json={"status": "Failed"},
        headers=auth_header(seeded_users["technician"]),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Failed"


# Auditor is read-only and should not be able to update status.
async def test_auditor_forbidden_from_updating_status(
    client,
    seeded_users,
    seeded_work_order,
):
    response = await client.patch(
        f"/work-orders/{seeded_work_order.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["auditor"]),
    )

    assert response.status_code == 403


# A work order that does not exist should return 404.
async def test_nonexistent_work_order_returns_404(
    client,
    seeded_users,
):
    response = await client.patch(
        "/work-orders/999999/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )

    assert response.status_code == 404