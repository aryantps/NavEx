from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.schemas.tenant import TenantCreate, TenantRead, TenantUpdate
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginatedQueryResponse
from app.db.repositories.tenant import TenantRepository
from app.db.session import get_db as get_session

router = APIRouter()

def get_tenant_repo(session=Depends(get_session)) -> TenantRepository:
    return TenantRepository(session)

@router.post("/", response_model=APIResponse[TenantRead], status_code=status.HTTP_201_CREATED)
async def create_tenant(
    data: TenantCreate,
    repo: TenantRepository = Depends(get_tenant_repo)
):
    tenant = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=tenant)

@router.get("/{id}", response_model=APIResponse[TenantRead])
async def get_tenant_by_id(
    id: int,
    repo: TenantRepository = Depends(get_tenant_repo)
):
    tenant = await repo.get(id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return APIResponse(success=True, code=200, data=tenant)

@router.get("/", response_model=APIResponse[PaginatedQueryResponse[TenantRead]])
async def list_tenants(
    name: Optional[str] = None,
    domain: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order_by: str = Query("id"),
    order_direction: str = Query("ASC", pattern="^(ASC|DESC)$"),
    repo: TenantRepository = Depends(get_tenant_repo),
):
    filters = {}
    if name:
        filters["name"] = name
    if domain:
        filters["domain"] = domain

    paginated = await repo.paginate_query(
        filters=filters,
        page=page,
        page_size=page_size,
        order_by=order_by,
        order_direction=order_direction,
    )

    return APIResponse(
        success=True,
        code=200,
        data=PaginatedQueryResponse[TenantRead](
            results=paginated["results"],
            pagination=paginated["pagination"]
        )
    )

@router.put("/{id}", response_model=APIResponse[TenantRead])
async def update_tenant(
    id: int,
    data: TenantUpdate,
    repo: TenantRepository = Depends(get_tenant_repo)
):
    updated = await repo.update(id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return APIResponse(success=True, code=200, data=updated)

@router.delete("/{id}", response_model=APIResponse[None])
async def delete_tenant(
    id: int,
    repo: TenantRepository = Depends(get_tenant_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return APIResponse(success=True, code=200, message="Deleted")

# TODO : Get current tenant from context
# context-aware endpoint for auth middleware
# /me or /current to get tenant of the logged-in user
