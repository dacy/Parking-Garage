from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    total_spaces = Column(Integer)
    available_spaces = Column(Integer)
    location = Column(String)
    building_to_garages = relationship("BuildingToGarage", back_populates="garage")
    spots = relationship("Spot", back_populates="garage")
    floors = relationship("Floor", back_populates="garage")
    entrance_to_garages = relationship("EntranceToGarage", back_populates="garage")
    zones = relationship("Zone", back_populates="garage")

class Floor(Base):
    __tablename__ = "floor"
    floor_id = Column(String, primary_key=True, index=True)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    floor_name = Column(String(100))
    capacity = Column(Integer)
    # Relationships
    garage = relationship("Garage", back_populates="floors")
    zones = relationship("Zone", back_populates="floor")
    spots = relationship("Spot", back_populates="floor")

class Zone(Base):
    __tablename__ = "zone"
    zone_id = Column(String, primary_key=True, index=True)
    floor_id = Column(String, ForeignKey("floor.floor_id"))
    garage_id = Column(Integer, ForeignKey("garages.id"))
    zone_name = Column(String(100))
    capacity = Column(Integer)
    # Relationships
    garage = relationship("Garage", back_populates="zones")
    floor = relationship("Floor", back_populates="zones")
    spots = relationship("Spot", back_populates="zone")

class Spot(Base):
    __tablename__ = "spot"
    spot_id = Column(String, primary_key=True, index=True)
    zone_id = Column(String, ForeignKey("zone.zone_id"))
    floor_id = Column(String, ForeignKey("floor.floor_id"))
    garage_id = Column(Integer, ForeignKey("garages.id"))
    is_occupied = Column(Boolean)
    restriction_type = Column(Integer)
    # Relationships
    zone = relationship("Zone", back_populates="spots")
    floor = relationship("Floor", back_populates="spots")
    garage = relationship("Garage", back_populates="spots")
    spot_changes = relationship("SpotChange", back_populates="spot")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    building_to_garages = relationship("BuildingToGarage", back_populates="building")

class BuildingToGarage(Base):
    __tablename__ = "building_to_garage"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    garage_id = Column(Integer, ForeignKey("garages.id"))
    distance = Column(Float)
    building = relationship("Building", back_populates="building_to_garages")
    garage = relationship("Garage", back_populates="building_to_garages")

class Entrance(Base):
    __tablename__ = "entrance"
    entrance_id = Column(String, primary_key=True, index=True)
    entrance_name = Column(String(100))
    # Relationships
    entrance_to_garages = relationship("EntranceToGarage", back_populates="entrance")

class EntranceToGarage(Base):
    __tablename__ = "entrance_to_garage"
    entrance_to_garage_id = Column(String, primary_key=True, index=True)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    entrance_id = Column(String, ForeignKey("entrance.entrance_id"))
    distance = Column(Float)
    # Relationships
    entrance = relationship("Entrance", back_populates="entrance_to_garages")
    garage = relationship("Garage", back_populates="entrance_to_garages")

class SpotChange(Base):
    __tablename__ = "spot_change"
    spot_change_id = Column(String, primary_key=True, index=True)
    spot_id = Column(String, ForeignKey("spot.spot_id"))
    is_parking = Column(Boolean)
    ts = Column(DateTime)
    # Relationships
    spot = relationship("Spot", back_populates="spot_changes")

class ParkingSpace(Base):
    __tablename__ = "parking_spaces"

    id = Column(Integer, primary_key=True, index=True)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    space_number = Column(String)
    is_available = Column(Boolean, default=True)
    is_reserved = Column(Boolean, default=False)
    last_used = Column(DateTime, nullable=True)
    garage = relationship("Garage") 