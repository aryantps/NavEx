from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)

    tenant = relationship("Tenant", back_populates="roles")
    users = relationship("UserRole", back_populates="role")
