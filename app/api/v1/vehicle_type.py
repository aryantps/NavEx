from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.db.repositories.vehicle_type import VehicleTypeRepository
from app.schemas.vehicle_type import (
    VehicleTypeCreate,
    VehicleTypeRead,
)
from app.db.session import get_db as get_session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/vehicle-types", tags=["Vehicle Types"])


# Dependency to inject the repository
def get_vehicle_type_repo(session=Depends(get_session)) -> VehicleTypeRepository:
    return VehicleTypeRepository(session)


@router.post("/", response_model=VehicleTypeRead)
async def create_vehicle_type_entry(
    data: VehicleTypeCreate,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    try:
        return await repo.create(data.dict())
    except IntegrityError as e:
        await repo.db.rollback()
        raise HTTPException(status_code=400, detail="Vehicle type with this code already exists.") from e


@router.get("/", response_model=List[VehicleTypeRead])
async def list_vehicle_type_entries(
    tenant: Optional[str] = None,
    is_active: Optional[bool] = True,
    type: Optional[str] = None,  # You can also use VehicleTypeEnum if needed
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo),
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if is_active is not None:
        filters["is_active"] = is_active
    if type is not None:
        filters["type"] = type

    return await repo.get_all(filters=filters)


@router.get("/{id}", response_model=VehicleTypeRead)
async def get_vehicle_type_entry_by_id(
    id: int,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    vehicle_type = await repo.get(id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return vehicle_type


@router.put("/{id}", response_model=VehicleTypeRead)
async def update_vehicle_type_entry(
    id: int,
    data: VehicleTypeCreate,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return updated


@router.patch("/{id}/deactivate", response_model=VehicleTypeRead)
async def deactivate_vehicle_type_entry(
    id: int,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    vehicle_type = await repo.get(id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")

    updated = await repo.update(id, {"is_active": False})
    return updated


@router.delete("/{id}")
async def delete_vehicle_type_entry(
    id: int,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return {"detail": "Deleted"}
