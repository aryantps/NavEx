from sqlalchemy import Column, Integer, ForeignKey, DateTime, PrimaryKeyConstraint, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

