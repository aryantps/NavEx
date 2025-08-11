from app.db.repositories.base import BaseRepository
from app.db.models.location import Location

class LocationRepository(BaseRepository[Location]):
    def __init__(self, session):
        super().__init__(db=session, model=Location)