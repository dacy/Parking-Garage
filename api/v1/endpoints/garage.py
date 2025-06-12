from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import models
from ..schemas import Garage, GarageSummary, Level, Zone, SpotTypeAvailability

router = APIRouter()

@router.get("/garages", response_model=list[GarageSummary])
def get_garages(db: Session = Depends(database.get_db)):
    garages = db.query(models.Garage).all()
    result = []
    
    for garage in garages:
        # Calculate available spots
        available_spots = sum(1 for spot in garage.spots if not spot.is_occupied)
        total_spots = len(garage.spots)
        
        # Calculate percentage
        percentage = (available_spots / total_spots * 100) if total_spots > 0 else 0
        
        # Create the response object
        garage_data = GarageSummary(
            id=garage.id,
            name=garage.name,
            total_capacity=garage.total_spaces,
            available_spots=available_spots,
            percentage=percentage
        )
        result.append(garage_data)
    
    return result

@router.get("/garages/{garage_id}", response_model=Garage)
def get_garage(garage_id: int, db: Session = Depends(database.get_db)):
    garage = db.query(models.Garage).filter(models.Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    # Get all floors for this garage
    floors = garage.floors
    level_list = []
    total_spots = len(garage.spots)
    total_available = sum(1 for spot in garage.spots if not spot.is_occupied)
    
    for floor in floors:
        spots = floor.spots
        available_spots = [s for s in spots if not s.is_occupied]
        
        # Group spots by zone
        zones = {}
        for spot in spots:
            zone = spot.zone
            if zone.zone_id not in zones:
                zones[zone.zone_id] = {
                    "name": zone.zone_name,
                    "spots": [],
                    "available": 0
                }
            zones[zone.zone_id]["spots"].append(spot)
            if not spot.is_occupied:
                zones[zone.zone_id]["available"] += 1
        
        # Convert zones to schema format
        zone_list = []
        for zone_id, zone_data in zones.items():
            spot_types = [
                SpotTypeAvailability(
                    type="Regular",  # You might want to map restriction_type to actual types
                    available=zone_data["available"]
                )
            ]
            zone_list.append(
                Zone(
                    name=zone_data["name"],
                    spot_types=spot_types
                )
            )
        
        level_list.append(
            Level(
                id=floor.floor_id,
                level=floor.floor_name,
                available_spaces=len(available_spots),
                percentage=(len(available_spots) / len(spots) * 100) if spots else 0,
                zones=zone_list
            )
        )
    
    percentage = (total_available / total_spots * 100) if total_spots else 0
    return Garage(
        id=garage.id,
        name=garage.name,
        total_capacity=garage.total_spaces,
        available_spots=total_available,
        percentage=percentage,
        levels=level_list
    ) 