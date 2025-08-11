from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.db.repositories.vehicle_type import VehicleTypeRepository
from app.schemas.vehicle_type import VehicleTypeCreate, VehicleTypeRead
from app.schemas.response import APIResponse
from app.db.session import get_db as get_session

router = APIRouter()


def get_vehicle_type_repo(session=Depends(get_session)) -> VehicleTypeRepository:
    return VehicleTypeRepository(session)


@router.post("/", response_model=APIResponse[VehicleTypeRead], status_code=status.HTTP_201_CREATED)
async def create_vehicle_type_entry(
    data: VehicleTypeCreate,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    vehicle_type = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=vehicle_type)


@router.get("/", response_model=APIResponse[List[VehicleTypeRead]])
async def list_vehicle_type_entries(
    tenant: Optional[str] = None,
    is_active: Optional[bool] = True,
    type: Optional[str] = None,  # Replace with VehicleTypeEnum if you want
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo),
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if is_active is not None:
        filters["is_active"] = is_active
    if type is not None:
        filters["type"] = type

    vehicle_types = await repo.get_all(filters=filters)
    return APIResponse(success=True, code=200, data=vehicle_types)


@router.get("/{id}", response_model=APIResponse[VehicleTypeRead])
async def get_vehicle_type_entry_by_id(
    id: int,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    vehicle_type = await repo.get(id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return APIResponse(success=True, code=200, data=vehicle_type)


@router.put("/{id}", response_model=APIResponse[VehicleTypeRead])
async def update_vehicle_type_entry(
    id: int,
    data: VehicleTypeCreate,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return APIResponse(success=True, code=200, data=updated)


@router.patch("/{id}/deactivate", response_model=APIResponse[VehicleTypeRead])
async def deactivate_vehicle_type_entry(
    id: int,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    vehicle_type = await repo.get(id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")

    updated = await repo.update(id, {"is_active": False})
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_vehicle_type_entry(
    id: int,
    repo: VehicleTypeRepository = Depends(get_vehicle_type_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    return APIResponse(success=True, code=200, message="Deleted")
