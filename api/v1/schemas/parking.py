from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class Building(str, Enum):
    A = "Building A"
    B = "Building B"
    C = "Building C"
    F = "Building F"

class Entrance(str, Enum):
    LEADERSHIP_DR = "Leadership Dr"
    HWY_121 = "Hwy 121"
    HEADQUARTER_DR = "Headquarters Dr"
    COMMUNICATION_PKWY = "Communication Pkwy"

class ParkingRequest(BaseModel):
    user_working_location: Building = Field(..., description="User working location building.")
    user_preferred_entrance: Entrance = Field(..., description="User's preferred entrance.")

class ParkingRecommendation(BaseModel):
    user_preferred_entrance: Entrance
    user_working_location: Building
    recommended_garage: str = Field(..., example="Garage C")
    recommended_garage_id: int = Field(..., example=3)
    recommended_floor: str = Field(..., example="Floor 3")
    recommended_floor_id: str = Field(..., example="F3_3")
    recommended_zone: str = Field(..., example="Zone A")
    recommended_zone_id: str = Field(..., example="Z3_3_A")
    availability_floor_percent: int = Field(..., example=85)
    availability_garage_percent: int = Field(..., example=70)

    class Config:
        from_attributes = True 