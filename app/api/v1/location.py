from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.db.repositories.location import LocationRepository
from app.schemas.location import LocationCreate, LocationRead
from app.schemas.response import APIResponse
from app.db.session import get_db as get_session

router = APIRouter(prefix="/locations", tags=["Locations"])


def get_location_repo(session=Depends(get_session)) -> LocationRepository:
    return LocationRepository(session)


@router.post("/", response_model=APIResponse[LocationRead], status_code=status.HTTP_201_CREATED)
async def create_location(
    data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repo)
):
    location = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=location)


@router.get("/", response_model=APIResponse[List[LocationRead]])
async def list_locations(
    tenant: Optional[str] = None,
    location_code: Optional[str] = None,
    location_name: Optional[str] = None,
    repo: LocationRepository = Depends(get_location_repo),
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if location_code is not None:
        filters["location_code"] = location_code
    if location_name is not None:
        filters["location_name"] = location_name

    locations = await repo.get_all(filters=filters)
    return APIResponse(success=True, code=200, data=locations)


@router.get("/{id}", response_model=APIResponse[LocationRead])
async def get_location_by_id(
    id: int,
    repo: LocationRepository = Depends(get_location_repo)
):
    location = await repo.get(id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return APIResponse(success=True, code=200, data=location)


@router.put("/{id}", response_model=APIResponse[LocationRead])
async def update_location(
    id: int,
    data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_location(
    id: int,
    repo: LocationRepository = Depends(get_location_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
    return APIResponse(success=True, code=200, message="Deleted")