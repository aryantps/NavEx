from app.db.repositories.base import BaseRepository
from app.db.models.user import User
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(db=session, model=User)

    async def get_user_with_roles_and_tenant(self, user_id: int):
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.roles), 
                selectinload(User.tenant)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()