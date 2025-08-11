from sqlalchemy import (
    Column, Integer, String, Boolean, Float, Text, TIMESTAMP,
    func, UniqueConstraint
)
from app.db.base_class import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    trip_code = Column(String(100), nullable=False, unique=True)
    status = Column(String(100), nullable=False)

    trip_start_time = Column(TIMESTAMP(timezone=True), nullable=True)
    trip_end_time = Column(TIMESTAMP(timezone=True), nullable=True)

    origin_name = Column(String(100), nullable=False)
    destination_name = Column(String(100), nullable=False)

    vehicle_code = Column(String(100), nullable=False)
    vehicle_number = Column(String(50), nullable=False)

    total_distance = Column(Float, nullable=True)
    total_trip_kms = Column(Float, default=0, nullable=False)
    total_time = Column(Float, nullable=True)
    tat = Column(Integer, nullable=True)

    driver_name = Column(String(100), nullable=True)
    driver_number = Column(String(100), nullable=True)

    started_by = Column(String(100), nullable=True)
    stopped_by = Column(String(100), nullable=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)

    client_name = Column(String(100), nullable=True)
    driver_consent_status = Column(String(200), nullable=True)
    shipment_codes = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)

    tenant = Column(String(100), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Trip(id={self.id}, code={self.trip_code}, status={self.status})>"
