from fastapi import FastAPI
from app.routers import equipment, work_order, auth

app = FastAPI(
    title="MedFlow Clinical Equipment Command Center",
    description="Clinical equipment management API for Halcyon Health Systems.",
    version="0.1.0" 
)

app.include_router(equipment.router)
app.include_router(work_order.router)
app.include_router(auth.router)



@app.get("/health", tags=["health"])
async def health_check() -> dict[str,str]:
    return {"status":"ok"}