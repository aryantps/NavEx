from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.db.session import get_db as get_session
from app.db.repositories.invitation import InvitationRepository
from app.schemas.invitation import (
    InvitationCreate,
    InvitationUpdate,
    InvitationRead,
)
from app.schemas.response import APIResponse
from app.schemas.pagination import PaginatedQueryResponse

router = APIRouter(prefix="/invitations", tags=["Invitations"])


def get_invitation_repo(session=Depends(get_session)) -> InvitationRepository:
    return InvitationRepository(session)


@router.post("/", response_model=APIResponse[InvitationRead], status_code=status.HTTP_201_CREATED)
async def create_invitation(
    data: InvitationCreate,
    repo: InvitationRepository = Depends(get_invitation_repo)
):
    # Optional: add business logic for checking duplicates or sending email
    invitation = await repo.create(data.dict())
    return APIResponse(success=True, code=201, data=invitation)


@router.get("/{id}", response_model=APIResponse[InvitationRead])
async def get_invitation_by_id(
    id: int,
    repo: InvitationRepository = Depends(get_invitation_repo)
):
    invitation = await repo.get(id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return APIResponse(success=True, code=200, data=invitation)


@router.get("/", response_model=APIResponse[PaginatedQueryResponse[InvitationRead]])
async def list_invitations(
    tenant_id: Optional[int] = None,
    email: Optional[str] = None,
    status: Optional[str] = None,  # e.g. pending, accepted, rejected
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order_by: str = Query("id"),
    order_direction: str = Query("ASC", pattern="^(ASC|DESC)$"),
    repo: InvitationRepository = Depends(get_invitation_repo),
):
    filters = {}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    if email is not None:
        filters["email"] = email
    if status is not None:
        filters["status"] = status

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
        data=PaginatedQueryResponse[InvitationRead](
            results=paginated["results"],
            pagination=paginated["pagination"]
        )
    )


@router.patch("/{id}", response_model=APIResponse[InvitationRead])
async def update_invitation_status(
    id: int,
    data: InvitationUpdate,  # expected to have status
    repo: InvitationRepository = Depends(get_invitation_repo)
):
    updated = await repo.update(id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return APIResponse(success=True, code=200, data=updated)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_invitation(
    id: int,
    repo: InvitationRepository = Depends(get_invitation_repo)
):
    success = await repo.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return APIResponse(success=True, code=200, message="Invitation revoked")
