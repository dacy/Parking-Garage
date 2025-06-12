from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import crud
import database

router = APIRouter()

@router.post("/parking/recommendation", response_model=schemas.ParkingRecommendation)
def get_parking_recommendation(request: schemas.ParkingRequest, db: Session = Depends(database.get_db)):
    """
    Provides a parking recommendation based on user's working location and preferred entrance.
    """
    return crud.get_parking_recommendation_from_db(
        db=db,
        working_location=request.user_working_location,
        preferred_entrance=request.user_preferred_entrance,
    ) 