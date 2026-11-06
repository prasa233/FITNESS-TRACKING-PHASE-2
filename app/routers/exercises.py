from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Exercise
from ..schemas import ExerciseCreate
from ..auth import get_current_user

router = APIRouter(
    prefix="/exercises",
    tags=["Exercise Library"]
)


@router.get("/")
def get_exercises(
    search: str = Query(default=""),
    category: str = Query(default=""),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Exercise)

    if search:
        query = query.filter(
            Exercise.name.ilike(f"%{search}%")
        )

    if category:
        query = query.filter(
            Exercise.category == category
        )

    return query.order_by(Exercise.name).all()


@router.post("/")
def create_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if data.category not in ["Cardio", "Strength", "Yoga"]:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Invalid exercise category"
        )

    exercise = Exercise(**data.model_dump())

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise