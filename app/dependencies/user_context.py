from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.repositories.user import UserRepository
from app.db.models.user import User

async def get_current_user_with_context(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_repo = UserRepository(db)
    user = await user_repo.get_user_with_roles_and_tenant(user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
