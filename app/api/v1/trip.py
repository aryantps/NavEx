from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.db.repositories.trip import TripRepository
from app.schemas.trip import TripCreate, TripRead
from app.db.session import get_db as get_session

router = APIRouter(prefix="/trips", tags=["Trips"])


# Dependency injection
def get_trip_repo(session=Depends(get_session)) -> TripRepository:
    return TripRepository(session)


@router.post("/", response_model=TripRead)
async def create_trip(
    data: TripCreate,
    repo: TripRepository = Depends(get_trip_repo)
):
    try:
        return await repo.create(data.dict())
    except IntegrityError:
        await repo.db.rollback()
        raise HTTPException(status_code=400, detail="Trip with this code already exists.")


@router.get("/", response_model=List[TripRead])
async def list_trips(
    tenant: Optional[str] = None,
    status: Optional[str] = None,
    vehicle_number: Optional[str] = None,
    repo: TripRepository = Depends(get_trip_repo)
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if status is not None:
        filters["status"] = status
    if vehicle_number is not None:
        filters["vehicle_number"] = vehicle_number

    return await repo.get_all(filters=filters)


@router.get("/{id}", response_model=TripRead)
async def get_trip_by_id(
    id: int,
    repo: TripRepository = Depends(get_trip_repo)
):
    trip = await repo.get(id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.put("/{id}", response_model=TripRead)
async def update_trip(
    id: int,
    data: TripCreate,
    repo: TripRepository = Depends(get_trip_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Trip not found")
    return updated


@router.patch("/{id}/close", response_model=TripRead)
async def close_trip(
    id: int,
    repo: TripRepository = Depends(get_trip_repo)
):
    trip = await repo.get(id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    updated = await repo.update(id, {"status": "completed", "trip_end_time": datetime.utcnow()})
    return updated


@router.delete("/{id}")
async def delete_trip(
    id: int,
    repo: TripRepository = Depends(get_trip_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"detail": "Deleted"}
