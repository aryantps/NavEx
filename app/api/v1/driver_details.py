from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.db.repositories.driver_details import DriverDetailRepository
from app.schemas.driver_details import DriverDetailCreate, DriverDetailRead
from app.db.session import get_db as get_session
from app.schemas.response import APIResponse

router = APIRouter()

def get_driver_repo(session=Depends(get_session)) -> DriverDetailRepository:
    return DriverDetailRepository(session)


@router.post("/", response_model=APIResponse[DriverDetailRead], status_code=status.HTTP_201_CREATED)
async def create_driver_detail(
    data: DriverDetailCreate,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    driver = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=driver)

@router.get("/", response_model=APIResponse[List[DriverDetailRead]])
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
    drivers = await repo.get_all(filters=filters)
    return APIResponse(success=True, code=200, data=drivers)


@router.get("/{id}", response_model=APIResponse[DriverDetailRead])
async def get_driver_detail_by_id(
    id: int,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    driver = await repo.get(id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return APIResponse(success=True, code=200, data=driver)


@router.put("/{id}", response_model=APIResponse[DriverDetailRead])
async def update_driver_detail(
    id: int,
    data: DriverDetailCreate,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    updated = await repo.update(id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Driver not found")
    return APIResponse(success=True, code=200, data=updated)


@router.patch("/{id}/deactivate", response_model=APIResponse[DriverDetailRead])
async def deactivate_driver_detail(
    id: int,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    driver = await repo.get(id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    updated = await repo.update(id, {"is_active": False})
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_driver_detail(
    id: int,
    repo: DriverDetailRepository = Depends(get_driver_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")
    return APIResponse(success=True, code=200, message="Deleted")
