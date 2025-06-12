from sqlalchemy.orm import Session
import models
from api.v1.schemas import Building, Entrance, ParkingRecommendation
from typing import Dict, List
import json

def build_llm_prompt(
    db: Session,
    user_working_location: Building,
    user_preferred_entrance: Entrance,
) -> str:
    # Get all garages
    garages = db.query(models.Garage).all()
    
    # Get the building - match the name exactly as stored in the database
    building = db.query(models.Building).filter(models.Building.name == user_working_location.value).first()
    if not building:
        raise ValueError(f"{user_working_location.value} not found in database")
    
    # Get the entrance - match the name exactly as stored in the database
    entrance = db.query(models.Entrance).filter(models.Entrance.entrance_name == user_preferred_entrance.value).first()
    if not entrance:
        raise ValueError(f"{user_preferred_entrance.value} not found in database")
    
    # Get all building to garage relationships
    building_to_garages = db.query(models.BuildingToGarage).filter(
        models.BuildingToGarage.building_id == building.id
    ).all()
    
    # Get all entrance to garage relationships
    entrance_to_garages = db.query(models.EntranceToGarage).filter(
        models.EntranceToGarage.entrance_id == entrance.entrance_id
    ).all()
    
    # Get all floors for each garage
    floors = {}
    for garage in garages:
        floors[garage.id] = db.query(models.Floor).filter(
            models.Floor.garage_id == garage.id
        ).all()
    
    # Get all zones for each floor
    zones = {}
    for floor_list in floors.values():
        for floor in floor_list:
            zones[floor.floor_id] = db.query(models.Zone).filter(
                models.Zone.floor_id == floor.floor_id
            ).all()
    
    # Get all spots for each zone
    spots = {}
    for zone_list in zones.values():
        for zone in zone_list:
            spots[zone.zone_id] = db.query(models.Spot).filter(
                models.Spot.zone_id == zone.zone_id
            ).all()
            
            # Get historical changes for each spot
            for spot in spots[zone.zone_id]:
                spot.historical_changes = db.query(models.SpotChange).filter(
                    models.SpotChange.spot_id == spot.spot_id
                ).order_by(models.SpotChange.ts.desc()).limit(5).all()
    
    # Build the prompt
    prompt = f"""Given the following parking garage information, recommend the best parking spot for a user working in {user_working_location.value} and preferring to enter from {user_preferred_entrance.value}.

Available Garages:
"""
    
    for garage in garages:
        prompt += f"\n{garage.name} (Total Spaces: {garage.total_spaces}, Available: {garage.available_spaces})"
        
        # Add building distances
        building_distances = [btg for btg in building_to_garages if btg.garage_id == garage.id]
        if building_distances:
            prompt += f"\n  Distance to {user_working_location.value}: {building_distances[0].distance} miles"
        
        # Add entrance distances
        entrance_distances = [etg for etg in entrance_to_garages if etg.garage_id == garage.id]
        if entrance_distances:
            prompt += f"\n  Distance to {user_preferred_entrance.value}: {entrance_distances[0].distance} miles"
        
        # Add floor information
        for floor in floors[garage.id]:
            prompt += f"\n  {floor.floor_name} (Capacity: {floor.capacity})"
            
            # Add zone information
            for zone in zones[floor.floor_id]:
                prompt += f"\n    {zone.zone_name} (Capacity: {zone.capacity})"
                
                # Add spot information
                occupied_count = sum(1 for spot in spots[zone.zone_id] if spot.is_occupied)
                restricted_count = sum(1 for spot in spots[zone.zone_id] if spot.restriction_type == 1)
                prompt += f"\n      Spots: {len(spots[zone.zone_id])} (Occupied: {occupied_count}, Restricted: {restricted_count})"
                
                # Add historical changes
                for spot in spots[zone.zone_id]:
                    if hasattr(spot, 'historical_changes') and spot.historical_changes:
                        prompt += f"\n      Spot {spot.spot_id} History:"
                        for change in spot.historical_changes:
                            status = "Parked" if change.is_parking else "Left"
                            prompt += f"\n        {status} at {change.ts}"
    
    prompt += "\n\nPlease recommend the best parking spot based on:\n"
    prompt += "1. Proximity to the user's building\n"
    prompt += "2. Proximity to the preferred entrance\n"
    prompt += "3. Current availability\n"
    prompt += "4. Historical parking patterns\n"
    prompt += "5. Restricted spots (if applicable)\n"
    
    return prompt

def get_ai_optimized_parking_recommendation(
    db: Session, working_location: Building, preferred_entrance: Entrance
) -> ParkingRecommendation:
    """
    Get AI-optimized parking recommendation based on current conditions and user preferences.
    """
    # Build the prompt for the LLM
    prompt = build_llm_prompt(db, working_location, preferred_entrance)
    
    # Log the prompt to console
    print("\n=== AI Parking Recommendation Prompt ===")
    print(prompt)
    print("=======================================\n")
    
    # TODO: Send prompt to LLM and process response
    # For now, return a mock recommendation
    return ParkingRecommendation(
        user_preferred_entrance=preferred_entrance,
        user_working_location=working_location,
        recommended_garage_and_floor="Garage A, Floor 1",  # This would come from LLM
        availability_floor_percent=85,  # This would come from LLM
        availability_garage_percent=70   # This would come from LLM
    ) 