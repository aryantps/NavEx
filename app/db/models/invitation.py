from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    email = Column(String, nullable=False)
    token = Column(String, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    invited_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    tenant = relationship("Tenant")
    role = relationship("Role")
    inviter = relationship("User", foreign_keys=[invited_by])
