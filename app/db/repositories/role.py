from app.db.repositories.base import BaseRepository
from app.db.models.role import Role

class RoleRepository(BaseRepository[Role]):
    def __init__(self, session):
        super().__init__(db=session, model=Role)