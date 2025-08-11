from sqlalchemy import (
    Column, Integer, String, Float, Text, TIMESTAMP,
    func, UniqueConstraint
)
from app.db.base_class import Base

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    tenant = Column(String(60), nullable=False)
    user_id = Column(String(100), nullable=True)

    location_code = Column(String(20), nullable=False)
    location_name = Column(String(100), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    city_name = Column(String(100), nullable=False)
    city_code = Column(String(10), nullable=True)

    state_name = Column(String(100), nullable=False)
    state_code = Column(String(10), nullable=True)

    district = Column(String(255), nullable=True)
    taluka = Column(String(255), nullable=True)
    zone = Column(String(255), nullable=True)
    area_office = Column(String(255), nullable=True)

    address = Column(Text, nullable=False)
    pincode = Column(String(6), nullable=False)

    location_type = Column(Integer, nullable=True)  # Could be FK or Enum

    gps_radius = Column(Integer, nullable=False, default=500)
    sim_radius = Column(Integer, nullable=False, default=5000)
    avg_loading_time = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('tenant', 'location_code', name='uq_location_tenant_code'),
        UniqueConstraint('tenant', 'location_name', name='uq_location_tenant_name'),
    )

    def __repr__(self):
        return f"<Location(id={self.id}, name={self.location_name}, code={self.location_code})>"
