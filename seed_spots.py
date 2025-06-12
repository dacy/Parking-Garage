import random
from sqlalchemy.orm import Session
import models
from database import SessionLocal

def seed_spots():
    """
    Seeds the database with parking spots for all zones based on a specified distribution.
    This function should be run once during the initial setup of the application.
    """
    db = SessionLocal()
    try:
        # Check if spots have already been seeded
        if db.query(models.Spot).first() is not None:
            print("Spots table is already populated. Skipping seeding.")
            return

        print("Seeding spots with specified distribution...")
        garages = db.query(models.Garage).all()
        for garage in garages:
            occupied_count_for_garage = 0
            
            floors = db.query(models.Floor).filter(models.Floor.garage_id == garage.id).all()
            for floor in floors:
                zones = db.query(models.Zone).filter(models.Zone.floor_id == floor.floor_id).all()
                for zone in zones:
                    for i in range(1, 51):  # 50 spots per zone
                        spot_id = f"S{garage.id}_{floor.floor_id.split('_')[1]}_{zone.zone_id.split('_')[2]}_{i}"

                        # 60% chance of being occupied
                        is_occupied = random.random() < 0.6
                        if is_occupied:
                            occupied_count_for_garage += 1

                        # Restriction type distribution: 10% type 1, 10% type 2, 80% type 0
                        restriction_roll = random.random()
                        if restriction_roll < 0.1:
                            restriction_type = 1
                        elif restriction_roll < 0.2:
                            restriction_type = 2
                        else:
                            restriction_type = 0

                        spot = models.Spot(
                            spot_id=spot_id,
                            zone_id=zone.zone_id,
                            floor_id=floor.floor_id,
                            garage_id=garage.id,
                            is_occupied=is_occupied,
                            restriction_type=restriction_type
                        )
                        db.add(spot)
            
            # Update the garage's available spaces based on the number of occupied spots created
            garage.available_spaces = garage.total_spaces - occupied_count_for_garage
            db.add(garage)

        db.commit()
        print("Successfully seeded all spots and updated garage availability.")

    except Exception as e:
        print(f"An error occurred during spot seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_spots() 