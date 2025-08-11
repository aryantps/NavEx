from app.db.repositories.base import BaseRepository
from app.db.models.user_role import UserRole

class UserRoleRepository(BaseRepository[UserRole]):
    def __init__(self, session):
        super().__init__(db=session, model=UserRole)