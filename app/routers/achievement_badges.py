from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AchievementBadge
from app.schemas import (
    AchievementBadgeCreate,
    AchievementBadgeResponse
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/achievement-badges",
    tags=["Achievement Badges"]
)


# Create Achievement Badge
@router.post("/", response_model=AchievementBadgeResponse)
def create_badge(
    data: AchievementBadgeCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    badge = AchievementBadge(
        user_id=user.id,
        name=data.name,
        description=data.description,
        badge_type=data.badge_type,
        icon=data.icon
    )

    db.add(badge)
    db.commit()
    db.refresh(badge)

    return badge


# Get All Achievement Badges
@router.get("/", response_model=list[AchievementBadgeResponse])
def get_badges(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return db.query(AchievementBadge).filter(
        AchievementBadge.user_id == user.id
    ).all()


# Get Badge By ID
@router.get("/{badge_id}", response_model=AchievementBadgeResponse)
def get_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    badge = db.query(AchievementBadge).filter(
        AchievementBadge.id == badge_id,
        AchievementBadge.user_id == user.id
    ).first()

    if not badge:
        raise HTTPException(
            status_code=404,
            detail="Achievement badge not found"
        )

    return badge


# Delete Achievement Badge
@router.delete("/{badge_id}")
def delete_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    badge = db.query(AchievementBadge).filter(
        AchievementBadge.id == badge_id,
        AchievementBadge.user_id == user.id
    ).first()

    if not badge:
        raise HTTPException(
            status_code=404,
            detail="Achievement badge not found"
        )

    db.delete(badge)
    db.commit()

    return {
        "message": "Achievement badge deleted successfully"
    }