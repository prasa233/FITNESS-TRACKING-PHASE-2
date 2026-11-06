from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Badge, UserBadge, WorkoutPlan


def award_badge(db: Session, user_id: int, badge_name: str):

    badge = db.query(Badge).filter(
        Badge.name == badge_name
    ).first()

    if not badge:
        return None

    existing = db.query(UserBadge).filter(
        UserBadge.user_id == user_id,
        UserBadge.badge_id == badge.id
    ).first()

    if existing:
        return existing

    user_badge = UserBadge(
        user_id=user_id,
        badge_id=badge.id
    )

    db.add(user_badge)

    try:
        db.commit()
        db.refresh(user_badge)
        return user_badge

    except IntegrityError:
        db.rollback()
        return None


def check_streak_badges(db: Session, user_id: int, streak: int):

    milestones = {
        3: "3-Day Warrior",
        7: "7-Day Warrior",
        30: "30-Day Warrior"
    }

    for days, badge_name in milestones.items():
        if streak >= days:
            award_badge(db, user_id, badge_name)


def check_workout_badges(
    db: Session,
    user_id: int,
    completed_workouts: int
):

    milestones = {
        1: "First Workout",
        5: "Fitness Starter",
        25: "Fitness Champion"
    }

    for count, badge_name in milestones.items():
        if completed_workouts >= count:
            award_badge(db, user_id, badge_name)