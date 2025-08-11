from app.db.repositories.base import BaseRepository
from app.db.models.trip import Trip

class TripRepository(BaseRepository[Trip]):
    def __init__(self, session):
        super().__init__(db=session, model=Trip)