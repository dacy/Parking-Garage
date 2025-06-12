from sqlalchemy.orm import Session
import models, schemas

def get_parking_recommendation_from_db(
    db: Session, working_location: schemas.Building, preferred_entrance: schemas.Entrance
) -> schemas.ParkingRecommendation:
    """
    This function queries the database to find the best parking spot.
    The logic here is a placeholder and should be adapted to your actual needs.
    """
    # Example: Query to get data from garage, floor, and spot tables
    # This is a placeholder query. You will need to adapt it to your schema and logic.
    best_spot = (
        db.query(models.Spot, models.Floor, models.Garage)
        .join(models.Floor, models.Spot.floor_id == models.Floor.id)
        .join(models.Garage, models.Floor.garage_id == models.Garage.id)
        .filter(models.Spot.is_available == 1)
        # Add more filtering logic here based on working_location and preferred_entrance
        .first()
    )

    if best_spot:
        spot_details, floor_details, garage_details = best_spot
        # This is where you would calculate percentages
        recommendation = schemas.ParkingRecommendation(
            user_preferred_entrance=preferred_entrance,
            user_working_location=working_location,
            recommended_garage_and_floor=f"{garage_details.name}, Floor {floor_details.level}",
            availability_floor_percent=90,  # Placeholder
            availability_garage_percent=75, # Placeholder
        )
    else:
        # Fallback if no spot is found
        recommendation = schemas.ParkingRecommendation(
            user_preferred_entrance=preferred_entrance,
            user_working_location=working_location,
            recommended_garage_and_floor="No recommendation available",
            availability_floor_percent=0,
            availability_garage_percent=0,
        )

    return recommendation 