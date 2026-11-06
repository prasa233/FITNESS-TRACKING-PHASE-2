from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import Badge, UserBadge
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/badges",
    tags=["Badges"]
)


@router.get("/")
def get_badges(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Badge).all()


@router.get("/my-badges")
def get_my_badges(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return (
        db.query(UserBadge)
        .filter(UserBadge.user_id == current_user.id)
        .all()
    )


@router.post("/award/{badge_id}")
def award_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    badge = db.query(Badge).filter(
        Badge.id == badge_id
    ).first()

    if badge is None:
        raise HTTPException(
            status_code=404,
            detail="Badge not found"
        )

    existing = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id,
        UserBadge.badge_id == badge_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Badge already awarded"
        )

    new_badge = UserBadge(
        user_id=current_user.id,
        badge_id=badge_id
    )

    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)

    return {
        "message": "Badge awarded successfully",
        "badge_id": badge_id
    }
    