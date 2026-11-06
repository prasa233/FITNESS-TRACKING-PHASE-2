from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/fitness",
    tags=["Fitness"]
)


@router.get("/")
def get_fitness(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {
        "status": "success",
        "message": "Fitness router working successfully",
        "user_id": current_user["id"]
    }


@router.get("/test")
def test_fitness():
    return {
        "status": "success",
        "message": "Fitness API is working"
    }