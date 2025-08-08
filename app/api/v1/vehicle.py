from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from app.db.repositories.vehicle import VehicleRepository
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleRead,
)
from app.db.session import get_db as get_session

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


# Dependency injection
def get_vehicle_repo(session=Depends(get_session)) -> VehicleRepository:
    return VehicleRepository(session)


@router.post("/", response_model=VehicleRead)
async def create_vehicle(
    data: VehicleCreate,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    try:
        return await repo.create(data.dict())
    except IntegrityError:
        await repo.db.rollback()
        raise HTTPException(status_code=400, detail="Vehicle with the same code or number already exists.")


@router.get("/", response_model=List[VehicleRead])
async def list_vehicles(
    tenant: Optional[str] = None,
    is_assigned: Optional[bool] = None,
    vehicle_type_id: Optional[int] = None,
    repo: VehicleRepository = Depends(get_vehicle_repo),
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if is_assigned is not None:
        filters["is_assigned"] = is_assigned
    if vehicle_type_id is not None:
        filters["vehicle_type_id"] = vehicle_type_id

    return await repo.get_all(filters=filters)


@router.get("/{id}", response_model=VehicleRead)
async def get_vehicle_by_id(
    id: int,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = await repo.get(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.put("/{id}", response_model=VehicleRead)
async def update_vehicle(
    id: int,
    data: VehicleCreate,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated


@router.patch("/{id}/deactivate", response_model=VehicleRead)
async def deactivate_vehicle(
    id: int,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = await repo.get(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    updated = await repo.update(id, {"is_assigned": False})
    return updated


@router.delete("/{id}")
async def delete_vehicle(
    id: int,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"detail": "Deleted"}
