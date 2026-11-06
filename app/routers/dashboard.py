from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from ..database import get_db
from ..models import WorkoutPlan, Streak, UserBadge
from ..auth import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Personalized Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = date.today()

    upcoming = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user.id,
        WorkoutPlan.scheduled_date >= today
    ).order_by(
        WorkoutPlan.scheduled_date
    ).limit(5).all()

    streak = db.query(Streak).filter(
        Streak.user_id == user.id
    ).first()

    badge_count = db.query(UserBadge).filter(
        UserBadge.user_id == user.id
    ).count()

    return {
        "user_id": user.id,
        "upcoming_workouts": upcoming,
        "current_streak": (
            streak.current_streak if streak else 0
        ),
        "longest_streak": (
            streak.longest_streak if streak else 0
        ),
        "total_badges": badge_count
    }