from app.db.repositories.base import BaseRepository
from app.db.models.tenant import Tenant

class TenantRepository(BaseRepository[Tenant]):
    def __init__(self, session):
        super().__init__(db=session, model=Tenant)