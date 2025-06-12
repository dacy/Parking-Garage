from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class Building(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    F = "F"

class Entrance(str, Enum):
    LEADERSHIP_DR = "Leadership Dr."
    HWY_121 = "Hwy 121"
    HEADQUARTER_DR = "Headquarter Dr."
    COMMUNICATION_PKWY = "Communication PKWY"

class ParkingRequest(BaseModel):
    user_working_location: Building = Field(..., description="User working location building.")
    user_preferred_entrance: Entrance = Field(..., description="User's preferred entrance.")

class ParkingRecommendation(BaseModel):
    user_preferred_entrance: Entrance
    user_working_location: Building
    recommended_garage_and_floor: str = Field(..., example="Garage C, Floor 3")
    availability_floor_percent: int = Field(..., example=85)
    availability_garage_percent: int = Field(..., example=70)

    class Config:
        from_attributes = True

class SpotTypeAvailability(BaseModel):
    type: str
    available: int

class Zone(BaseModel):
    name: str
    spot_types: List[SpotTypeAvailability]

class Level(BaseModel):
    id: str
    level: str
    available_spaces: int
    percentage: float
    zones: List[Zone]

class Garage(BaseModel):
    id: str
    name: str
    total_capacity: int
    available_spots: int = 0
    percentage: float = 0
    levels: Optional[List[Level]] = None
    
    class Config:
        from_attributes = True

class GarageSummary(BaseModel):
    id: str
    name: str
    total_capacity: int
    available_spots: int = 0
    percentage: float = 0
    
    class Config:
        from_attributes = True 