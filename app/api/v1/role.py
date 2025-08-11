from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.db.session import get_db as get_session
from app.db.repositories.role import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate, RoleRead
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginatedQueryResponse

router = APIRouter()


def get_role_repo(session=Depends(get_session)) -> RoleRepository:
    return RoleRepository(session)


@router.post("/", response_model=APIResponse[RoleRead], status_code=status.HTTP_201_CREATED)
async def create_role(
    data: RoleCreate,
    repo: RoleRepository = Depends(get_role_repo)
):
    role = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=role)


@router.get("/{id}", response_model=APIResponse[RoleRead])
async def get_role(
    id: int,
    repo: RoleRepository = Depends(get_role_repo)
):
    role = await repo.get(id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return APIResponse(success=True, code=200, data=role)


@router.get("/", response_model=APIResponse[PaginatedQueryResponse[RoleRead]])
async def list_roles(
    name: Optional[str] = None,
    tenant_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order_by: str = Query("id"),
    order_direction: str = Query("ASC", pattern="^(ASC|DESC)$"),
    repo: RoleRepository = Depends(get_role_repo),
):
    filters = {}
    if name is not None:
        filters["name"] = name
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id

    paginated = await repo.paginate_query(
        filters=filters,
        page=page,
        page_size=page_size,
        order_by=order_by,
        order_direction=order_direction
    )

    return APIResponse(
        success=True,
        code=200,
        data=PaginatedQueryResponse[RoleRead](
            results=paginated["results"],
            pagination=paginated["pagination"]
        )
    )


@router.put("/{id}", response_model=APIResponse[RoleRead])
async def update_role(
    id: int,
    data: RoleUpdate,
    repo: RoleRepository = Depends(get_role_repo)
):
    updated = await repo.update(id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_role(
    id: int,
    repo: RoleRepository = Depends(get_role_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return APIResponse(success=True, code=200, message="Role deleted")
