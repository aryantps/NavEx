from sqlalchemy import (
    Column, Integer, String, Boolean, Numeric, TIMESTAMP, CheckConstraint,
    Enum as SAEnum, func
)
from app.db.base_class import Base
from sqlalchemy.orm import relationship
import enum



class VehicleTypeEnum(str, enum.Enum):
    CAR = "car"
    TRUCK = "truck"
    VAN = "van"


class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(SAEnum(VehicleTypeEnum), nullable=False)
    code = Column(String(80), nullable=False, unique=True, index=True)
    tenant = Column(String(50), nullable=False)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    length = Column(Numeric(10, 2), nullable=False)
    breadth = Column(Numeric(10, 2), nullable=False)
    height = Column(Numeric(10, 2), nullable=False)
    load_capacity = Column(Numeric(10, 2), nullable=True)

    vehicles = relationship("Vehicle", back_populates="vehicle_type", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('length > 0', name='check_length_positive'),
        CheckConstraint('breadth > 0', name='check_breadth_positive'),
        CheckConstraint('height > 0', name='check_height_positive'),
    )

    def __repr__(self):
        return f"<VehicleType(id={self.id}, type={self.type}, code={self.code})>"