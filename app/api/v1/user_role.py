from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.db.session import get_db as get_session
from app.db.repositories.user_role import UserRoleRepository
from app.schemas.user_role import UserRoleCreate, UserRoleRead
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginatedQueryResponse

router = APIRouter()


def get_user_role_repo(session=Depends(get_session)) -> UserRoleRepository:
    return UserRoleRepository(session)


@router.post("/", response_model=APIResponse[UserRoleRead], status_code=status.HTTP_201_CREATED)
async def assign_role_to_user(
    data: UserRoleCreate,
    repo: UserRoleRepository = Depends(get_user_role_repo)
):
    user_role = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=user_role)


@router.get("/by-user/{user_id}", response_model=APIResponse[List[UserRoleRead]])
async def get_roles_for_user(
    user_id: int,
    repo: UserRoleRepository = Depends(get_user_role_repo)
):
    filters = {"user_id": user_id}
    user_roles = await repo.get_all(filters=filters)
    return APIResponse(success=True, code=200, data=user_roles)


@router.get("/", response_model=APIResponse[PaginatedQueryResponse[UserRoleRead]])
async def list_user_roles(
    user_id: Optional[int] = None,
    role_id: Optional[int] = None,
    tenant_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order_by: str = Query("id"),
    order_direction: str = Query("ASC", pattern="^(ASC|DESC)$"),
    repo: UserRoleRepository = Depends(get_user_role_repo),
):
    filters = {}
    if user_id is not None:
        filters["user_id"] = user_id
    if role_id is not None:
        filters["role_id"] = role_id
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
        data=PaginatedQueryResponse[UserRoleRead](
            results=paginated["results"],
            pagination=paginated["pagination"]
        )
    )


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_user_role(
    id: int,
    repo: UserRoleRepository = Depends(get_user_role_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="User-Role mapping not found")
    return APIResponse(success=True, code=200, message="Mapping deleted")
