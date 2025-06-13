import random
import time
import uuid
from sqlalchemy.orm import Session
from datetime import datetime

# Adjust imports to work with our project structure
from database import SessionLocal
from models import Spot, SpotChange

def get_random_spot_ids(db: Session, n: int):
    """
    Gets a specified number of random spot IDs from the database.
    """
    all_spots = db.query(Spot.spot_id).all()
    # The result of the query is a list of tuples, e.g., [('S1_1_1_1',), ('S1_1_1_2',)]
    # We need to extract the first element from each tuple.
    spot_ids = [spot[0] for spot in all_spots]
    
    # Ensure we don't try to sample more spots than exist
    sample_size = min(n, len(spot_ids))
    if sample_size == 0:
        return []
    
    return random.sample(spot_ids, sample_size)

def update_parking_status(db: Session, spot_id: str, is_parking: bool):
    """
    Updates the occupancy status of a single spot and records the event in SpotChange.
    """
    spot = db.query(Spot).filter(Spot.spot_id == spot_id).first()
    if spot:
        # Prevent creating a change if the state is not actually different
        if spot.is_occupied == is_parking:
            print(f"Spot {spot_id} is already {'occupied' if is_parking else 'vacant'}. No change made.")
            return

        spot.is_occupied = is_parking

        # Create a new SpotChange entry
        spot_change = SpotChange(
            spot_change_id=str(uuid.uuid4()),  # Generate a unique ID for the change
            spot_id=spot_id,
            is_parking=is_parking,
            ts=datetime.now()
        )
        db.add(spot_change)
        
        print(f"Updated spot {spot_id} to {'occupied' if is_parking else 'vacant'}.")
    else:
        print(f"Spot {spot_id} not found.")

def run_simulation(num_updates: int = 5):
    """
    Main function to run the simulation.
    Fetches a number of random spots and updates their status.
    """
    print("-" * 30)
    print(f"Running parking simulation for {num_updates} spot(s)...")
    
    db = SessionLocal()
    try:
        random_spot_ids = get_random_spot_ids(db, num_updates)
        if not random_spot_ids:
            print("No spots found in the database to update.")
            return

        for spot_id in random_spot_ids:
            # Always simulate a parking event (occupying a spot)
            is_parking_event = True
            update_parking_status(db, spot_id, is_parking_event)
        
        # Commit all the changes made in this session
        db.commit()
        print("Simulation complete. All changes committed.")
    
    except Exception as e:
        print(f"An error occurred during the simulation: {e}")
        db.rollback()
    finally:
        db.close()
    print("-" * 30)

if __name__ == "__main__":
    # This script will now run in a continuous loop.
    # Press Ctrl+C to stop the simulation.
    try:
        while True:
            # You can change num_updates to control how many spots are changed each cycle.
            run_simulation(num_updates=40)
            # Wait for 5 seconds before the next cycle.
            print("\nNext update in 3 seconds... (Press Ctrl+C to stop)")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.") 