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
        percentage = round((available_spots / total_spots * 100), 2) if total_spots > 0 else 0
        
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
        # For each floor, process its zones to get detailed availability
        processed_zones = []
        for zone_model in floor.zones:
            spots_in_zone = zone_model.spots
            
            # Calculate total available spots and percentage for this specific zone
            total_spots_in_zone = len(spots_in_zone)
            total_available_in_zone = sum(1 for s in spots_in_zone if not s.is_occupied)
            zone_percentage = round((total_available_in_zone / total_spots_in_zone * 100), 2) if total_spots_in_zone > 0 else 0
            
            # Group available spots by their restriction type
            available_by_type = {}
            for spot in spots_in_zone:
                if not spot.is_occupied:
                    r_type = spot.restriction_type
                    available_by_type[r_type] = available_by_type.get(r_type, 0) + 1
            
            # Map integer restriction types to human-readable names
            spot_type_map = {0: "Regular", 1: "Compact", 2: "Handicap"}
            spot_types_list = [
                SpotTypeAvailability(
                    type=spot_type_map.get(r_type, f"Unknown Type {r_type}"),
                    available=count
                )
                for r_type, count in available_by_type.items()
            ]
            
            # Create the Zone object for the response
            processed_zone = Zone(
                name=zone_model.zone_name,
                available_spaces=total_available_in_zone,
                percentage=zone_percentage,
                spot_types=spot_types_list
            )
            processed_zones.append(processed_zone)

        # Calculate floor-level statistics
        total_spots_in_floor = len(floor.spots)
        total_available_in_floor = sum(1 for s in floor.spots if not s.is_occupied)
        
        level_list.append(
            Level(
                id=floor.floor_id,
                level=floor.floor_name,
                available_spaces=total_available_in_floor,
                percentage=round((total_available_in_floor / total_spots_in_floor * 100), 2) if total_spots_in_floor else 0,
                zones=processed_zones
            )
        )
    
    percentage = round((total_available / total_spots * 100), 2) if total_spots else 0
    return Garage(
        id=garage.id,
        name=garage.name,
        total_capacity=garage.total_spaces,
        available_spots=total_available,
        percentage=percentage,
        levels=level_list
    ) 