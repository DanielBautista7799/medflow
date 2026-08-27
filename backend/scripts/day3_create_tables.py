from app.models.base import Base
from app.database import engine

from app.models.hospital import Hospital
from app.models.equipment import Equipment
from app.models.work_order import WorkOrder
from app.models.service_report import ServiceReport

import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())