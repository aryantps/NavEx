from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from app.db.repositories.driver_details import DriverDetailRepository
from app.schemas.driver_details import (
    DriverDetailCreate,
    DriverDetailRead,
)
from app.core.logger import logger
from app.db.session import get_db as get_session

router = APIRouter(prefix="/drivers", tags=["Drivers"])


# Dependency injection for the repository
def get_driver_repo(session=Depends(get_session)) -> DriverDetailRepository:
    return DriverDetailRepository(session)


@router.post("/", response_model=DriverDetailRead)
async def create_driver_detail(
    data: DriverDetailCreate,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    try:
        return await repo.create(data.dict())
    except IntegrityError:
        await repo.db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate driver record for tenant/license or external ID.")


@router.get("/", response_model=List[DriverDetailRead])
async def list_driver_details(
    tenant: Optional[str] = None,
    is_active: Optional[bool] = True,
    license_number: Optional[str] = None,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    filters = {}
    if tenant is not None:
        filters["tenant"] = tenant
    if is_active is not None:
        filters["is_active"] = is_active
    if license_number is not None:
        filters["license_number"] = license_number

    return await repo.get_all(filters=filters)


@router.get("/{id}", response_model=DriverDetailRead)
async def get_driver_detail_by_id(
    id: int,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    logger.info("Fetching driver list")
    driver = await repo.get(id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.put("/{id}", response_model=DriverDetailRead)
async def update_driver_detail(
    id: int,
    data: DriverDetailCreate,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Driver not found")
    return updated


@router.patch("/{id}/deactivate", response_model=DriverDetailRead)
async def deactivate_driver_detail(
    id: int,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    driver = await repo.get(id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    updated = await repo.update(id, {"is_active": False})
    return updated


@router.delete("/{id}")
async def delete_driver_detail(
    id: int,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"detail": "Deleted"}
