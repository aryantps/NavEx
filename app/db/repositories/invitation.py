from app.db.repositories.base import BaseRepository
from app.db.models.invitation import Invitation

class InvitationRepository(BaseRepository[Invitation]):
    def __init__(self, session):
        super().__init__(db=session, model=Invitation)