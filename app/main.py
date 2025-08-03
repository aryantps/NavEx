from fastapi import FastAPI
from app.api.v1 import trip, eta, tracking, master_data

app = FastAPI(title="Logistics Management API")

app.include_router(trip.router, prefix="/api/v1/trips", tags=["Trips"])
app.include_router(eta.router, prefix="/api/v1/eta", tags=["ETA"])
app.include_router(tracking.router, prefix="/api/v1/tracking", tags=["Tracking"])
app.include_router(master_data.router, prefix="/api/v1/masters", tags=["Master Data"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
