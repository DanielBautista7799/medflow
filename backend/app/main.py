from fastapi import FastAPI

app = FastAPI(
    title="MedFlow Clinical Equipment Command Center",
    description="Clinical equipment management API for Halcyon Health Systems.",
    version="0.1.0" 
)

@app.get("/health", tags=["health"])
async def health_check() -> dict[str,str]:
    return {"status":"ok"}