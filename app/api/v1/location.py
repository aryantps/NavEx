from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from app.db.repositories.location import LocationRepository
from app.schemas.location import (
    LocationCreate,
    LocationRead,
)
from app.db.session import get_db as get_session

router = APIRouter(prefix="/locations", tags=["Locations"])


# Dependency injection for the repository
def get_location_repo(session=Depends(get_session)) -> LocationRepository:
    return LocationRepository(session)


@router.post("/", response_model=LocationRead)
async def create_location(
    data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repo)
):
    try:
        return await repo.create(data.dict())
    except IntegrityError:
        await repo.db.rollback()
        raise HTTPException(status_code=400, detail="Location with this code or name already exists.")


@router.get("/", response_model=List[LocationRead])
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

    return await repo.get_all(filters=filters)


@router.get("/{id}", response_model=LocationRead)
async def get_location_by_id(
    id: int,
    repo: LocationRepository = Depends(get_location_repo)
):
    location = await repo.get(id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{id}", response_model=LocationRead)
async def update_location(
    id: int,
    data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated


@router.delete("/{id}")
async def delete_location(
    id: int,
    repo: LocationRepository = Depends(get_location_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"detail": "Deleted"}
