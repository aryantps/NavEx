from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.db.repositories.vehicle import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleRead
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginatedQueryResponse
from app.db.session import get_db as get_session

router = APIRouter()


def get_vehicle_repo(session=Depends(get_session)) -> VehicleRepository:
    return VehicleRepository(session)


@router.post("/", response_model=APIResponse[VehicleRead], status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    data: VehicleCreate,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=vehicle)


@router.get("/", response_model=APIResponse[List[VehicleRead]])
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

    vehicles = await repo.get_all(filters=filters)
    return APIResponse(success=True, code=200, data=vehicles)

@router.get("/paginated", response_model=APIResponse[PaginatedQueryResponse[VehicleRead]])
async def list_vehicles_paginated(
    tenant: Optional[str] = None,
    is_assigned: Optional[bool] = None,
    vehicle_type_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 10,
    order_by: str = "id",
    order_direction: str = Query("ASC", pattern="^(ASC|DESC)$"),
    repo: VehicleRepository = Depends(get_vehicle_repo),
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if is_assigned is not None:
        filters["is_assigned"] = is_assigned
    if vehicle_type_id is not None:
        filters["vehicle_type_id"] = vehicle_type_id

    paginated_result = await repo.paginate_query(
        filters=filters,
        page=page,
        page_size=page_size,
        order_by=order_by,
        order_direction=order_direction
    )

    return APIResponse(
        success=True,
        code=200,
        data=PaginatedQueryResponse[VehicleRead](
            results=paginated_result["results"],
            pagination=paginated_result["pagination"]
        )
    )

@router.get("/{id}", response_model=APIResponse[VehicleRead])
async def get_vehicle_by_id(
    id: int,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = await repo.get(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return APIResponse(success=True, code=200, data=vehicle)


@router.put("/{id}", response_model=APIResponse[VehicleRead])
async def update_vehicle(
    id: int,
    data: VehicleCreate,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return APIResponse(success=True, code=200, data=updated)


@router.patch("/{id}/deactivate", response_model=APIResponse[VehicleRead])
async def deactivate_vehicle(
    id: int,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    vehicle = await repo.get(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    updated = await repo.update(id, {"is_assigned": False})
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_vehicle(
    id: int,
    repo: VehicleRepository = Depends(get_vehicle_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return APIResponse(success=True, code=200, message="Deleted")