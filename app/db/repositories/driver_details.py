from app.db.repositories.base import BaseRepository
from app.db.models.driver_details import DriverDetail

class DriverDetailRepository(BaseRepository[DriverDetail]):
    def __init__(self, session):
        super().__init__(db=session, model=DriverDetail)