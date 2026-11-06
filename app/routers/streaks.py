from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from ..database import get_db
from ..models import Streak
from ..auth import get_current_user

router = APIRouter(
    prefix="/streaks",
    tags=["Streak Tracking"]
)


@router.post("/record")
def record_workout(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = date.today()

    streak = db.query(Streak).filter(
        Streak.user_id == user.id
    ).first()

    if not streak:
        streak = Streak(
            user_id=user.id,
            current_streak=1,
            longest_streak=1,
            last_workout_date=today
        )
        db.add(streak)

    elif streak.last_workout_date == today:
        return {
            "message": "Today's workout already recorded",
            "current_streak": streak.current_streak
        }

    elif streak.last_workout_date == today - timedelta(days=1):
        streak.current_streak += 1
        streak.last_workout_date = today

    else:
        streak.current_streak = 1
        streak.last_workout_date = today

    streak.longest_streak = max(
        streak.longest_streak,
        streak.current_streak
    )

    db.commit()
    db.refresh(streak)

    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak
    }


@router.get("/")
def get_streak(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    streak = db.query(Streak).filter(
        Streak.user_id == user.id
    ).first()

    if not streak:
        return {
            "current_streak": 0,
            "longest_streak": 0
        }

    return streak