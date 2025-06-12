from pydantic import BaseModel, Field
from typing import List, Optional

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
    id: int
    name: str
    total_capacity: int
    available_spots: int = 0
    percentage: float = 0
    levels: Optional[List[Level]] = None
    
    class Config:
        from_attributes = True

class GarageSummary(BaseModel):
    id: int
    name: str
    total_capacity: int
    available_spots: int = 0
    percentage: float = 0
    
    class Config:
        from_attributes = True 