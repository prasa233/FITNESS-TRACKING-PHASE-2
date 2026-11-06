from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Workout
from ..auth import get_current_user

router = APIRouter(
    prefix="/progress",
    tags=["Progress Comparison"]
)


@router.get("/weekly")
def weekly_progress(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = datetime.now()
    start = today - timedelta(days=7)
    previous_start = today - timedelta(days=14)

    current_count = db.query(func.count(Workout.id)).filter(
        Workout.user_id == user.id,
        Workout.created_at >= start
    ).scalar() or 0

    previous_count = db.query(func.count(Workout.id)).filter(
        Workout.user_id == user.id,
        Workout.created_at >= previous_start,
        Workout.created_at < start
    ).scalar() or 0

    improvement = current_count - previous_count

    return {
        "current_week": current_count,
        "previous_week": previous_count,
        "improvement": improvement
    }


@router.get("/monthly")
def monthly_progress(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = datetime.now()
    start = today - timedelta(days=30)
    previous_start = today - timedelta(days=60)

    current_count = db.query(func.count(Workout.id)).filter(
        Workout.user_id == user.id,
        Workout.created_at >= start
    ).scalar() or 0

    previous_count = db.query(func.count(Workout.id)).filter(
        Workout.user_id == user.id,
        Workout.created_at >= previous_start,
        Workout.created_at < start
    ).scalar() or 0

    return {
        "current_month": current_count,
        "previous_month": previous_count,
        "improvement": current_count - previous_count
    }