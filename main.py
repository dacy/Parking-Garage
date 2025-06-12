from fastapi import FastAPI
from sqlalchemy import text
from database import engine, Base
from api.v1.endpoints import parking
from api.v1.endpoints import garage
import models  # Ensures models are registered with SQLAlchemy

app = FastAPI(
    title="Parking Recommendation API",
    description="API to provide parking recommendations based on user location and entrance preference.",
    version="1.0.0",
)

# Create tables and load data before including routers
Base.metadata.create_all(bind=engine)

# Load initial data
raw_conn = engine.raw_connection()
try:
    with open("init.sql", "r") as f:
        sql_script = f.read()
        raw_conn.executescript(sql_script)
    print("Successfully loaded init.sql")
except FileNotFoundError:
    print("init.sql not found, skipping. Database will be empty.")
except Exception as e:
    print(f"An error occurred while executing init.sql: {e}")
finally:
    raw_conn.close()

# Include routers after database initialization
app.include_router(parking.router, prefix="/api/v1", tags=["Parking"])
app.include_router(garage.router, prefix="/api/v1", tags=["Garage"])

@app.on_event("startup")
async def startup_event():
    # Any additional startup tasks can go here
    pass

@app.on_event("shutdown")
def shutdown_event():
    from database import engine, Base
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.") 