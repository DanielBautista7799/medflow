"""
MedFlow Command Center
Day 10 - endpoint tests for /equipment.
"""

from tests.conftest import auth_header


# No authorization header should be rejected.
async def test_list_equipment_requires_authentication(client):
    response = await client.get("/equipment")

    assert response.status_code == 401


# Auditor is authenticated and should be allowed to read equipment.
async def test_list_equipment_any_authenticated_role(
    client,
    seeded_users,
):
    response = await client.get(
        "/equipment",
        headers=auth_header(seeded_users["auditor"]),
    )

    assert response.status_code == 200


# Field Technician is logged in but should not be allowed to create equipment.
async def test_create_equipment_forbidden_for_field_technician(
    client,
    seeded_users,
    seeded_hospital,
):
    payload = {
        "serial_number": "TX-1001",
        "model": "Test-Device",
        "charge_level": 50,
        "facility_id": seeded_hospital.id,
        "status": "Available",
    }

    response = await client.post(
        "/equipment",
        json=payload,
        headers=auth_header(seeded_users["technician"]),
    )

    assert response.status_code == 403


# Clinical Admin should be allowed to create equipment.
async def test_create_equipment_succeeds_for_clinical_admin(
    client,
    seeded_users,
    seeded_hospital,
):
    payload = {
        "serial_number": "TX-1001",
        "model": "Test-Device",
        "charge_level": 50,
        "facility_id": seeded_hospital.id,
        "status": "Available",
    }

    response = await client.post(
        "/equipment",
        json=payload,
        headers=auth_header(seeded_users["admin"]),
    )

    assert response.status_code == 201
    assert response.json()["serial_number"] == "TX-1001"


# max_charge should only return equipment at or below the given charge level.
async def test_low_charge_filter(
    client,
    seeded_users,
    seeded_hospital,
):
    admin_headers = auth_header(seeded_users["admin"])

    low = {
        "serial_number": "LOW-01",
        "model": "Test-Device",
        "charge_level": 10,
        "facility_id": seeded_hospital.id,
        "status": "Available",
    }

    high = {
        "serial_number": "HIGH-01",
        "model": "Test-Device",
        "charge_level": 90,
        "facility_id": seeded_hospital.id,
        "status": "Available",
    }

    await client.post(
        "/equipment",
        json=low,
        headers=admin_headers,
    )

    await client.post(
        "/equipment",
        json=high,
        headers=admin_headers,
    )

    response = await client.get(
        "/equipment?max_charge=20",
        headers=admin_headers,
    )

    serials = [
        equipment["serial_number"]
        for equipment in response.json()
    ]

    assert "LOW-01" in serials
    assert "HIGH-01" not in serials