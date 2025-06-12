from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import models
import schemas

router = APIRouter()

@router.get("/garages", response_model=list[schemas.GarageSummary])
def get_garages(db: Session = Depends(database.get_db)):
    garages = db.query(models.Garage).all()
    result = []
    
    for garage in garages:
        # Calculate available spots
        available_spots = 0
        total_spots = 0
        
        # Calculate percentage
        percentage = (available_spots / total_spots * 100) if total_spots > 0 else 0
        
        # Create the response object with available_spots (no levels)
        garage_data = schemas.GarageSummary(
            id=garage.id,
            name=garage.name,
            location=garage.location,
            total_capacity=garage.total_capacity,
            available_spots=available_spots,
            percentage=percentage
        )
        result.append(garage_data)
    
    return result

@router.get("/garages/{garage_id}", response_model=schemas.Garage)
def get_garage_detail(garage_id: int, db: Session = Depends(database.get_db)):
    garage = db.query(models.Garage).filter(models.Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    # Get all levels (floors) for this garage
    floors = db.query(models.Floor).filter(models.Floor.garage_id == garage_id).all()
    level_list = []
    total_spots = 0
    total_available = 0
    for floor in floors:
        spots = db.query(models.Spot).filter(models.Spot.floor_id == floor.id).all()
        available_spots = [s for s in spots if s.is_available]
        total_spots += len(spots)
        total_available += len(available_spots)
        # For now, treat each floor as a single zone named 'Zone 1'
        type_counts = {"Compact": 0, "Regular": 0, "Handicapped": 0}
        type_available = {"Compact": 0, "Regular": 0, "Handicapped": 0}
        for s in spots:
            spot_type = getattr(s, "type", "Regular")
            if spot_type not in type_counts:
                type_counts[spot_type] = 0
                type_available[spot_type] = 0
            type_counts[spot_type] += 1
            if s.is_available:
                type_available[spot_type] += 1
        spot_types = [
            schemas.SpotTypeAvailability(type=spot_type, available=type_available[spot_type])
            for spot_type in type_counts
        ]
        zones = [schemas.Zone(name="Zone 1", spot_types=spot_types)]
        level_list.append(
            schemas.Level(
                id=floor.id,
                level=floor.level,
                available_spaces=len(available_spots),
                percentage=(len(available_spots) / len(spots) * 100) if spots else 0,
                zones=zones
            )
        )
    percentage = (total_available / total_spots * 100) if total_spots else 0
    return schemas.Garage(
        id=garage.id,
        name=garage.name,
        location=garage.location,
        total_capacity=garage.total_capacity,
        available_spots=total_available,
        percentage=percentage,
        levels=level_list
    ) 