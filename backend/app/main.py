from app.config import settings

from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from app.routers import equipment, work_order, auth

FRONTEND_ORIGIN = settings.frontend_origin

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



# BEGIN EXCEPTIONS

# Handles database constraint errors such as duplicate unique values.
@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": "A database constraint was violated (e.g. a duplicate value)"
        },
    )



# Handles database constraint errors such as duplicate unique values.
@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": "A database constraint was violated (e.g. a duplicate value)"
        },
    )


# Catch-all for unexpected errors so the API always returns clean JSON.
@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error has occurred."},
    )