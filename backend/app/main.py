import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import equipment, work_order, auth

FRONTEND_ORIGIN = os.environ.get(
    "FRONTEND_ORIGIN",
    "http://localhost:5173"
)

app = FastAPI(
    title="MedFlow Clinical Equipment Command Center",
    description="Clinical equipment management API for Halcyon Health Systems.",
    version="0.2.0" 
)

# CORS is like a checkpoint between the frontend and backend.
# It lets the browser know which frontend origins, methods, and headers are allowed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(equipment.router)
app.include_router(work_order.router)
app.include_router(auth.router)




@app.get("/health", tags=["health"])
async def health_check() -> dict[str,str]:
    return {"status":"ok"}

@app.get("/version", tags=["health"])
async def version() -> dict[str, str]:
    return {"version": app.version}