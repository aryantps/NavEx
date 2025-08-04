from app.db.repositories.base import BaseRepository
from app.db.models.vehicle_type import VehicleType

class VehicleTypeRepository(BaseRepository[VehicleType]):
    def __init__(self, session):
        super().__init__(VehicleType, session)