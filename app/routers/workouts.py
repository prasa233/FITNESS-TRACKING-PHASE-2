from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


@router.get("/")
def get_workouts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "Workout router working successfully",
        "user_id": current_user["id"]
    }


@router.get("/test")
def test_workouts():
    return {
        "status": "success",
        "message": "Workouts API is working"
    }