from pydantic import BaseModel, confloat
from typing import Optional
from datetime import datetime
from enum import Enum

class TrackingTypeEnum(str, Enum):
    GPS = "GPS"
    SIM = "SIM"
    TELENITY = "TELENITY"
    OTHER = "OTHER"

class VehicleTrackingBase(BaseModel):
    vehicle_id: int
    tracking_type: TrackingTypeEnum
    provider_name: Optional[str]
    device_id: str
    sim_number: Optional[str]
    latitude: Optional[confloat(ge=-90, le=90)]
    longitude: Optional[confloat(ge=-180, le=180)]
    speed: Optional[float]
    accuracy: Optional[float]
    last_update_time: Optional[datetime]
    is_active: bool = True

class VehicleTrackingCreate(VehicleTrackingBase):
    pass

class VehicleTrackingRead(VehicleTrackingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class VehicleTrackingPing(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)
    speed: Optional[float]
    accuracy: Optional[float]
