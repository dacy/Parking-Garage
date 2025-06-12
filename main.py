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

app.include_router(parking.router, prefix="/api/v1", tags=["Parking"])
app.include_router(garage.router, prefix="/api/v1", tags=["Garage"])

@app.on_event("startup")
def startup_event():
    # Create tables defined by SQLAlchemy models
    Base.metadata.create_all(bind=engine)

    # --- Place to load your SQL file ---
    # You can load and execute your custom SQL script here.
    # For example, if you have an 'init.sql' file in the same directory:
    with engine.connect() as connection:
        try:
            with open("init.sql", "r") as f:
                sql_script = f.read()
                with connection.begin():
                    connection.execute(text(sql_script))
            print("Successfully loaded init.sql")
        except FileNotFoundError:
            print("init.sql not found, skipping. Database will be empty.")
        except Exception as e:
            print(f"An error occurred while executing init.sql: {e}") 