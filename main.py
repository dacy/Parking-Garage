from fastapi import FastAPI
from sqlalchemy import text
from database import engine, Base, SessionLocal
from api.v1.endpoints import parking, garage
import models  # Ensures models are registered with SQLAlchemy
from seed_spots import seed_spots

app = FastAPI(
    title="Parking Recommendation API",
    description="API to provide parking recommendations based on user location and entrance preference.",
    version="1.0.0",
)

# --- Database Initialization ---
def initialize_database():
    # First, ensure all tables are created. This is safe to run every time.
    print("Ensuring all tables are created...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    db = SessionLocal()
    try:
        # Now that tables exist, check if they are empty
        if db.query(models.Building).first() is not None:
            print("Database already contains data. Skipping initialization.")
            return

        # If we're here, the database is empty and needs to be seeded
        print("Database is empty. Seeding initial data...")
        
        # Load base data from init.sql
        with open("init.sql", "r") as f:
            sql_script = f.read()
        
        with engine.connect() as connection:
            dbapi_conn = connection.connection
            try:
                cursor = dbapi_conn.cursor()
                cursor.executescript(sql_script)
                dbapi_conn.commit()
                print("Successfully executed init.sql")
            finally:
                cursor.close()

        # Seed the spots
        seed_spots()

    except FileNotFoundError:
        print("init.sql not found, skipping basic data load.")
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

# Run initialization on startup
initialize_database()


# --- API Routers ---
app.include_router(parking.router, prefix="/api/v1", tags=["Parking"])
app.include_router(garage.router, prefix="/api/v1", tags=["Garage"])

@app.on_event("startup")
async def startup_event():
    # Additional startup tasks can go here
    pass

@app.on_event("shutdown")
def shutdown_event():
    from database import engine, Base
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.") 