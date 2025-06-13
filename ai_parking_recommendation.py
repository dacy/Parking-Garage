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
        # --- Garage-level calculation ---
        all_spots_in_garage = [spot for floor in floors[garage.id] for zone in zones[floor.floor_id] for spot in spots[zone.zone_id]]
        total_spots_garage = len(all_spots_in_garage)
        available_spots_garage = sum(1 for s in all_spots_in_garage if not s.is_occupied)
        garage_percentage = round((available_spots_garage / total_spots_garage * 100), 2) if total_spots_garage > 0 else 0
        prompt += f"\n{garage.name} ({garage_percentage}% Available - {available_spots_garage}/{total_spots_garage} Total)"

        building_distances = [btg for btg in building_to_garages if btg.garage_id == garage.id]
        if building_distances:
            prompt += f"\n  Distance to {user_working_location.value}: {building_distances[0].distance} miles"
        
        entrance_distances = [etg for etg in entrance_to_garages if etg.garage_id == garage.id]
        if entrance_distances:
            prompt += f"\n  Distance to {user_preferred_entrance.value}: {entrance_distances[0].distance} miles"
        
        # --- Floor-level loop ---
        for floor in floors[garage.id]:
            all_spots_in_floor = [spot for zone in zones[floor.floor_id] for spot in spots[zone.zone_id]]
            total_spots_floor = len(all_spots_in_floor)
            available_spots_floor = sum(1 for s in all_spots_in_floor if not s.is_occupied)
            floor_percentage = round((available_spots_floor / total_spots_floor * 100), 2) if total_spots_floor > 0 else 0
            prompt += f"\n  {floor.floor_name} ({floor_percentage}% Available)"
            
            # --- Zone-level loop ---
            for zone in zones[floor.floor_id]:
                spots_in_zone = spots[zone.zone_id]
                total_spots_zone = len(spots_in_zone)
                available_spots_zone = sum(1 for s in spots_in_zone if not s.is_occupied)
                zone_percentage = round((available_spots_zone / total_spots_zone * 100), 2) if total_spots_zone > 0 else 0
                prompt += f"\n    {zone.zone_name} ({zone_percentage}% Available)"
                
                # Group spots by restriction_type and occupancy
                spot_counts = {0: {"total": 0, "occupied": 0}, 1: {"total": 0, "occupied": 0}, 2: {"total": 0, "occupied": 0}}
                for spot in spots_in_zone:
                    r_type = spot.restriction_type
                    if r_type in spot_counts:
                        spot_counts[r_type]["total"] += 1
                        if spot.is_occupied:
                            spot_counts[r_type]["occupied"] += 1

                # Create a detailed spot breakdown string
                spot_type_map = {0: "Regular", 1: "Compact", 2: "Handicap"}
                breakdown_parts = []
                for r_type, counts in spot_counts.items():
                    if counts["total"] > 0:
                        breakdown_parts.append(f"{spot_type_map.get(r_type)}: {counts['occupied']}/{counts['total']}")
                
                spot_breakdown_str = ", ".join(breakdown_parts)
                prompt += f"\n      Spots: {spot_breakdown_str}"
                
                # Add historical changes
                for spot in spots_in_zone:
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
        recommended_garage="Garage A",  # This would come from LLM
        recommended_garage_id=1,  # This would come from LLM
        recommended_floor="Floor 1",  # This would come from LLM
        recommended_floor_id="F1_1",  # This would come from LLM
        recommended_zone="Zone 1",  # This would come from LLM
        recommended_zone_id="Z1_1_1",  # This would come from LLM
        availability_floor_percent=85,  # This would come from LLM
        availability_garage_percent=70   # This would come from LLM
    ) 