from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import ai_parking_recommendation
from ..schemas import ParkingRequest, ParkingRecommendation

router = APIRouter()

@router.post("/parking/recommendation", response_model=ParkingRecommendation)
def recommend_parking(
    request: ParkingRequest, db: Session = Depends(database.get_db)
):
    recommendation = ai_parking_recommendation.get_ai_optimized_parking_recommendation(
        db, request.user_working_location, request.user_preferred_entrance
    )
    return recommendation 