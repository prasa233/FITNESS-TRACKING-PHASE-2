from datetime import date, timedelta

from sqlalchemy.orm import Session
from app.models import Streak


def update_streak(db: Session, user_id: int):

    today = date.today()

    streak = db.query(Streak).filter(
        Streak.user_id == user_id
    ).first()

    if not streak:
        streak = Streak(
            user_id=user_id,
            current_streak=1,
            longest_streak=1,
            last_workout_date=today
        )

        db.add(streak)
        db.commit()
        db.refresh(streak)

        return streak

    if streak.last_workout_date == today:
        return streak

    yesterday = today - timedelta(days=1)

    if streak.last_workout_date == yesterday:
        streak.current_streak += 1
    else:
        streak.current_streak = 1

    streak.longest_streak = max(
        streak.current_streak,
        streak.longest_streak
    )

    streak.last_workout_date = today

    db.commit()
    db.refresh(streak)

    return streak