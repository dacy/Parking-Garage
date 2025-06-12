from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    total_capacity = Column(Integer)
    # Add other garage fields here

class Floor(Base):
    __tablename__ = "floors"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    # Add other floor fields here

class Spot(Base):
    __tablename__ = "spots"
    id = Column(Integer, primary_key=True, index=True)
    spot_number = Column(String)
    floor_id = Column(Integer, ForeignKey("floors.id"))
    is_available = Column(Integer) # Using Integer to represent boolean for simplicity
    type = Column(String, default="Regular") # Compact, Regular, Handicapped
    # Add other spot fields here 