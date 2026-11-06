from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, timedelta

from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/comparison",
    tags=["Progress Comparison"]
)


def get_stats(db, user_id, start_date, end_date):
    result = db.execute(
        text("""
            SELECT
                COUNT(*) AS total_workouts,
                COALESCE(SUM(duration), 0) AS total_duration
            FROM workouts
            WHERE user_id = :user_id
            AND workout_date >= :start_date
            AND workout_date < :end_date
            AND status = 'COMPLETED'
        """),
        {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date
        }
    ).mappings().first()

    return {
        "total_workouts": result["total_workouts"],
        "total_duration": result["total_duration"]
    }


@router.get("/weekly")
def weekly_comparison(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    today = date.today()

    current_start = today - timedelta(days=today.weekday())
    next_week = current_start + timedelta(days=7)
    previous_start = current_start - timedelta(days=7)

    current = get_stats(
        db, user_id, current_start, next_week
    )

    previous = get_stats(
        db, user_id, previous_start, current_start
    )

    return {
        "current_week": current,
        "previous_week": previous,
        "workout_difference": (
            current["total_workouts"] -
            previous["total_workouts"]
        ),
        "duration_difference": (
            current["total_duration"] -
            previous["total_duration"]
        )
    }


@router.get("/monthly")
def monthly_comparison(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    today = date.today()

    current_start = today.replace(day=1)

    previous_end = current_start
    previous_start = (
        (current_start - timedelta(days=1)).replace(day=1)
    )

    next_month = (
        (current_start.replace(day=28) + timedelta(days=4))
        .replace(day=1)
    )

    current = get_stats(
        db, user_id, current_start, next_month
    )

    previous = get_stats(
        db, user_id, previous_start, previous_end
    )

    return {
        "current_month": current,
        "previous_month": previous,
        "workout_difference": (
            current["total_workouts"] -
            previous["total_workouts"]
        )
    }