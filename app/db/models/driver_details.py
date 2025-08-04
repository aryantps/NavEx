from sqlalchemy import (
    Column, Integer, String, Boolean, Text, TIMESTAMP,
    UniqueConstraint, func
)
from app.db.base_class import Base


class DriverDetail(Base):
    __tablename__ = "driver_details"

    id = Column(Integer, primary_key=True, index=True)
    tenant = Column(Text, nullable=False)
    driver_name = Column(Text, nullable=False)
    contact_number = Column(Text, nullable=True)
    driver_address = Column(Text, nullable=True)
    ext_driver_id = Column(Text, nullable=True, unique=True)
    license_number = Column(Text, nullable=False)
    license_expiry = Column(TIMESTAMP(timezone=True), nullable=True)
    license_issue = Column(TIMESTAMP(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    pincode = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_dedicated = Column(Boolean, default=False, nullable=False)
    location_code = Column(Text, nullable=True)
    location_name = Column(Text, nullable=True)
    is_assigned = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint('tenant', 'license_number', name='uq_driver_tenant_license'),
        UniqueConstraint('ext_driver_id', 'tenant', name='uq_ext_driver_id_tenant'),
    )

    def __repr__(self):
        return f"<DriverDetail(id={self.id}, name={self.driver_name}, license={self.license_number})>"
