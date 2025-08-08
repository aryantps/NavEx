from app.db.repositories.base import BaseRepository
from app.db.models.vehicle import Vehicle

class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, session):
        super().__init__(db=session, model=Vehicle)