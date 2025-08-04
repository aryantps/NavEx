from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Enum, ForeignKey,
    TIMESTAMP, func
)
from app.db.base_class import Base
import enum

class TrackingTypeEnum(str, enum.Enum):
    GPS = "GPS"
    SIM = "SIM"
    TELENITY = "TELENITY"
    OTHER = "OTHER"

class VehicleTracking(Base):
    __tablename__ = "vehicle_tracking"

    id = Column(Integer, primary_key=True, index=True)
    
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    tracking_type = Column(Enum(TrackingTypeEnum), nullable=False)
    provider_name = Column(String(100), nullable=True)
    
    device_id = Column(String(100), nullable=False)  # IMEI, asset ID, etc.
    sim_number = Column(String(20), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)

    last_update_time = Column(TIMESTAMP(timezone=True), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<VehicleTracking(vehicle_id={self.vehicle_id}, type={self.tracking_type}, device_id={self.device_id})>"
