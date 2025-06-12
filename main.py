from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey
from database import engine, Base
from api.v1.endpoints import parking
import models

# In-memory SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Placeholder SQLAlchemy models for your tables
# You can replace these with your actual table schemas
class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
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
    # Add other spot fields here

app = FastAPI(
    title="Parking Recommendation API",
    description="API to provide parking recommendations based on user location and entrance preference.",
    version="1.0.0",
)

app.include_router(parking.router, prefix="/api/v1", tags=["Parking"])

@app.on_event("startup")
def startup_event():
    # Create tables defined by SQLAlchemy models
    Base.metadata.create_all(bind=engine)

    # --- Place to load your SQL file ---
    # You can load and execute your custom SQL script here.
    # For example, if you have an 'init.sql' file in the same directory:
    with engine.connect() as connection:
        try:
            with open("init.sql", "r") as f:
                sql_script = f.read()
                # Using text() to indicate this is a SQL string
                # For this to work, you need to commit the transaction
                with connection.begin():
                    connection.execute(text(sql_script))
            print("Successfully loaded init.sql")
        except FileNotFoundError:
            print("init.sql not found, skipping. Database will be empty.")
        except Exception as e:
            print(f"An error occurred while executing init.sql: {e}")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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


def get_parking_recommendation_from_db(
    db: Session, working_location: Building, preferred_entrance: Entrance
) -> ParkingRecommendation:
    """
    This function queries the database to find the best parking spot.
    The logic here is a placeholder and should be adapted to your actual needs.
    """
    # Example: Query to get data from garage, floor, and spot tables
    # This is a placeholder query. You will need to adapt it to your schema and logic.
    best_spot = (
        db.query(Spot, Floor, Garage)
        .join(Floor, Spot.floor_id == Floor.id)
        .join(Garage, Floor.garage_id == Garage.id)
        .filter(Spot.is_available == 1)
        # Add more filtering logic here based on working_location and preferred_entrance
        .first()
    )

    if best_spot:
        spot_details, floor_details, garage_details = best_spot
        # This is where you would calculate percentages
        recommendation = ParkingRecommendation(
            user_preferred_entrance=preferred_entrance,
            user_working_location=working_location,
            recommended_garage_and_floor=f"{garage_details.name}, Floor {floor_details.level}",
            availability_floor_percent=90,  # Placeholder
            availability_garage_percent=75, # Placeholder
        )
    else:
        # Fallback if no spot is found
        recommendation = ParkingRecommendation(
            user_preferred_entrance=preferred_entrance,
            user_working_location=working_location,
            recommended_garage_and_floor="No recommendation available",
            availability_floor_percent=0,
            availability_garage_percent=0,
        )

    return recommendation


@app.post("/parking/recommendation", response_model=ParkingRecommendation)
def get_parking_recommendation(request: ParkingRequest, db: Session = Depends(get_db)):
    """
    Provides a parking recommendation based on user's working location and preferred entrance.
    """
    recommendation = get_parking_recommendation_from_db(
        db=db,
        working_location=request.user_working_location,
        preferred_entrance=request.user_preferred_entrance,
    )
    return recommendation 