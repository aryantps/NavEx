from app.utils.utils import create_vehicle_id
from sqlalchemy import (
    Column, Integer, String, Boolean, Numeric, TIMESTAMP,
    ForeignKey, UniqueConstraint, CheckConstraint, Index,
    Enum as SAEnum, func
)
from app.db.base_class import Base
from sqlalchemy.orm import relationship
import enum


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    id = Column(String(50), primary_key=True, default=create_vehicle_id)
    vehicle_number = Column(String(50), nullable=False)
    vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id", ondelete="CASCADE"), nullable=False)
    is_assigned = Column(Boolean, default=False, nullable=False)
    tenant = Column(String(50), nullable=False)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    vehicle_code = Column(String(100), nullable=False, unique=True, index=True)
    tracking_asset_id = Column(Integer, nullable=True)
    rc_number = Column(String(100), nullable=True)
    puc_number = Column(String(100), nullable=True)

    vehicle_type = relationship("VehicleType", back_populates="vehicles")

    __table_args__ = (
        UniqueConstraint('vehicle_number', 'tenant', name='vehicles_vehicle_number_tenant_key'),
        Index('idx_vehicles_tracking_asset_id', 'tracking_asset_id'),
        Index('idx_vehicles_vehicle_code', 'vehicle_code'),
        Index('idx_vehicles_vehicle_number', 'vehicle_number'),
    )

    def __repr__(self):
        return f"<Vehicle(id={self.id}, vehicle_number={self.vehicle_number}, code={self.vehicle_code})>"
