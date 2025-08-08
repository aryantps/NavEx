from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.db.repositories.vehicle_tracking import VehicleTrackingRepository
from app.schemas.vehicle_tracking import (
    VehicleTrackingCreate,
    VehicleTrackingRead,
    VehicleTrackingPing,
    TrackingTypeEnum,
)
from app.db.session import get_db as get_session  # get_session returns an `AsyncSession`

router = APIRouter(prefix="/tracking-records", tags=["Vehicle Tracking"])


def get_tracking_repo(session=Depends(get_session)) -> VehicleTrackingRepository:
    return VehicleTrackingRepository(session)


@router.post("/", response_model=VehicleTrackingRead)
async def create_vehicle_tracking_entry(
    data: VehicleTrackingCreate,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo)
):
    return await repo.create(data.dict())


@router.get("/", response_model=List[VehicleTrackingRead])
async def list_vehicle_tracking_entries(
    vehicle_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    tracking_type: Optional[TrackingTypeEnum] = None,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo),
):
    filters = {}
    if vehicle_id is not None:
        filters["vehicle_id"] = vehicle_id
    if is_active is not None:
        filters["is_active"] = is_active
    if tracking_type is not None:
        filters["tracking_type"] = tracking_type

    return await repo.get_all(filters=filters)


@router.get("/{id}", response_model=VehicleTrackingRead)
async def get_vehicle_tracking_entry_by_id(
    id: int,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo)
):
    tracking = await repo.get(id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return tracking


@router.put("/{id}", response_model=VehicleTrackingRead)
async def update_vehicle_tracking_entry(
    id: int,
    data: VehicleTrackingCreate,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return updated


@router.patch("/{id}/deactivate", response_model=VehicleTrackingRead)
async def deactivate_vehicle_tracking_entry(
    id: int,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo)
):
    tracking = await repo.get(id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")

    updated = await repo.update(id, {"is_active": False})
    return updated


@router.delete("/{id}")
async def delete_vehicle_tracking_entry(
    id: int,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return {"detail": "Deleted"}


@router.patch("/{id}/ping", response_model=VehicleTrackingRead)
async def record_vehicle_tracking_ping(
    id: int,
    ping: VehicleTrackingPing,
    repo: VehicleTrackingRepository = Depends(get_tracking_repo)
):
    tracking = await repo.get(id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")

    data = ping.dict()
    data["last_update_time"] = ping.timestamp or None
    updated = await repo.update(id, data)
    return updated
