from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.dependencies.user_context import get_current_user_with_context
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginatedQueryResponse
from app.db.repositories.user import UserRepository
from app.db.session import get_db as get_session
from app.db.models.user import User

router = APIRouter()


def get_user_repo(session=Depends(get_session)) -> UserRepository:
    return UserRepository(session)


@router.post("/", response_model=APIResponse[UserRead], status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    repo: UserRepository = Depends(get_user_repo)
):
    user = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=user)


@router.get("/{id}", response_model=APIResponse[UserRead])
async def get_user_by_id(
    id: int,
    repo: UserRepository = Depends(get_user_repo)
):
    user = await repo.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(success=True, code=200, data=user)


@router.get("/", response_model=APIResponse[PaginatedQueryResponse[UserRead]])
async def list_users(
    tenant_id: Optional[int] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order_by: str = Query("id"),
    order_direction: str = Query("ASC", pattern="^(ASC|DESC)$"),
    repo: UserRepository = Depends(get_user_repo),
):
    filters = {}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    if email is not None:
        filters["email"] = email
    if is_active is not None:
        filters["is_active"] = is_active

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
        data=PaginatedQueryResponse[UserRead](
            results=paginated["results"],
            pagination=paginated["pagination"]
        )
    )


@router.put("/{id}", response_model=APIResponse[UserRead])
async def update_user(
    id: int,
    data: UserUpdate,
    repo: UserRepository = Depends(get_user_repo)
):
    updated = await repo.update(id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_user(
    id: int,
    repo: UserRepository = Depends(get_user_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(success=True, code=200, message="Deleted")


@router.get("/me", response_model=APIResponse[dict])
async def get_current_user(
    current_user: User = Depends(get_current_user_with_context)
):
    return APIResponse(
        success=True,
        code=200,
        data={
            "user_id": current_user.id,
            "email": current_user.email,
            "roles": [role.name for role in current_user.roles],
            "tenant": current_user.tenant.name if current_user.tenant else None
        }
    )