from app.db.repositories.base import BaseRepository
from app.db.models.vehicle_tracking import VehicleTracking

class VehicleTrackingRepository(BaseRepository[VehicleTracking]):
    def __init__(self, session):
        super().__init__(VehicleTracking, session)