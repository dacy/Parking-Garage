from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Garage(Base):
    __tablename__ = "garage"
    garage_id = Column(String, primary_key=True, index=True)  # UUID as string
    garage_name = Column(String(100))
    capacity = Column(Integer)
    # Relationships
    floors = relationship("Floor", back_populates="garage")
    zones = relationship("Zone", back_populates="garage")
    spots = relationship("Spot", back_populates="garage")

class Floor(Base):
    __tablename__ = "floor"
    floor_id = Column(String, primary_key=True, index=True)  # UUID as string
    garage_id = Column(String, ForeignKey("garage.garage_id"))
    floor_name = Column(String(100))
    capacity = Column(Integer)
    # Relationships
    garage = relationship("Garage", back_populates="floors")
    zones = relationship("Zone", back_populates="floor")
    spots = relationship("Spot", back_populates="floor")

class Zone(Base):
    __tablename__ = "zone"
    zone_id = Column(String, primary_key=True, index=True)  # UUID as string
    floor_id = Column(String, ForeignKey("floor.floor_id"))
    garage_id = Column(String, ForeignKey("garage.garage_id"))
    zone_name = Column(String(100))
    capacity = Column(Integer)
    # Relationships
    garage = relationship("Garage", back_populates="zones")
    floor = relationship("Floor", back_populates="zones")
    spots = relationship("Spot", back_populates="zone")

class Spot(Base):
    __tablename__ = "spot"
    spot_id = Column(String, primary_key=True, index=True)  # UUID as string
    zone_id = Column(String, ForeignKey("zone.zone_id"))
    floor_id = Column(String, ForeignKey("floor.floor_id"))
    garage_id = Column(String, ForeignKey("garage.garage_id"))
    is_occupied = Column(Boolean)
    restriction_type = Column(Integer)
    # Relationships
    garage = relationship("Garage", back_populates="spots")
    floor = relationship("Floor", back_populates="spots")
    zone = relationship("Zone", back_populates="spots")
    spot_changes = relationship("SpotChange", back_populates="spot")

class Building(Base):
    __tablename__ = "building"
    building_id = Column(String, primary_key=True, index=True)  # UUID as string
    building_name = Column(String(100))
    # Relationships
    building_to_garages = relationship("BuildingToGarage", back_populates="building")

class BuildingToGarage(Base):
    __tablename__ = "building_to_garage"
    building_to_garage_id = Column(String, primary_key=True, index=True)  # UUID as string
    garage_id = Column(String, ForeignKey("garage.garage_id"))
    building_id = Column(String, ForeignKey("building.building_id"))
    distance = Column(String)  # Type is ambiguous in SQL, using String
    # Relationships
    building = relationship("Building", back_populates="building_to_garages")
    garage = relationship("Garage")

class Entrance(Base):
    __tablename__ = "entrance"
    entrance_id = Column(String, primary_key=True, index=True)  # UUID as string
    entrance_name = Column(String(100))
    # Relationships
    entrance_to_garages = relationship("EntranceToGarage", back_populates="entrance")

class EntranceToGarage(Base):
    __tablename__ = "entrance_to_garage"
    entrance_to_garage_id = Column(String, primary_key=True, index=True)  # UUID as string
    garage_id = Column(String, ForeignKey("garage.garage_id"))
    entrance_id = Column(String, ForeignKey("entrance.entrance_id"))
    distance = Column(String)  # Type is ambiguous in SQL, using String
    # Relationships
    entrance = relationship("Entrance", back_populates="entrance_to_garages")
    garage = relationship("Garage")

class SpotChange(Base):
    __tablename__ = "spot_change"
    spot_change_id = Column(String, primary_key=True, index=True)  # UUID as string
    spot_id = Column(String, ForeignKey("spot.spot_id"))
    is_parking = Column(Boolean)
    ts = Column(DateTime)
    # Relationships
    spot = relationship("Spot", back_populates="spot_changes") 