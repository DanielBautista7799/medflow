"""
MedFlow Command Center
Day 10 - shared pytest fixtures.

Creates:
- isolated local test database sessions
- FastAPI test client
- fake users for each RBAC role
- fake hospital data
- JWT authorization headers
"""

import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.dependencies import get_db
from app.main import app
from app.models import Base, Hospital, User, UserRole
from app.security import create_access_token, hash_password


TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://danielbautista@127.0.0.1:5432/medflow_test",
)


# Separate database engine used only by tests.
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


# Creates all tables before each test and drops them afterward.
# This means every test starts with a completely clean database.
@pytest_asyncio.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Makes FastAPI use medflow_test instead of the normal database.
@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# Creates one fake user for each MedFlow RBAC role.
@pytest_asyncio.fixture
async def seeded_users(db_session):
    users = {
        "admin": User(
            username="test_admin",
            hashed_password=hash_password("pw"),
            role=UserRole.CLINICAL_ADMIN,
        ),
        "technician": User(
            username="test_technician",
            hashed_password=hash_password("pw"),
            role=UserRole.FIELD_TECHNICIAN,
        ),
        "auditor": User(
            username="test_auditor",
            hashed_password=hash_password("pw"),
            role=UserRole.AUDITOR,
        ),
    }

    for user in users.values():
        db_session.add(user)

    await db_session.commit()

    for user in users.values():
        await db_session.refresh(user)

    return users


# Creates one fake hospital for equipment that requires a valid facility_id.
@pytest_asyncio.fixture
async def seeded_hospital(db_session):
    hospital = Hospital(
        name="Test Hospital",
        location_region="Test Region",
        capacity=10,
        supervisor_id=1,
    )

    db_session.add(hospital)
    await db_session.commit()
    await db_session.refresh(hospital)

    return hospital


# Creates a real JWT for whichever fake user the test wants to act as.
def auth_header(user: User) -> dict[str, str]:
    token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role.value,
        }
    )

    return {
        "Authorization": f"Bearer {token}"
    }