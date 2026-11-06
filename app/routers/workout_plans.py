

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import WorkoutPlan
from ..database import get_db
from ..schemas import WorkoutPlanCreate
from ..auth import get_current_user


router = APIRouter(
    prefix="/workout-plans",
    tags=["Workout Plans"]
)


# CREATE WORKOUT PLAN
@router.post("/")
def create_plan(
    data: WorkoutPlanCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    plan = WorkoutPlan(
        user_id=user.id,
        title=data.title,
        description=data.description,
        scheduled_date=data.scheduled_date
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return {
        "message": "Workout plan created successfully",
        "id": plan.id,
        "user_id": plan.user_id,
        "title": plan.title,
        "description": plan.description,
        "scheduled_date": plan.scheduled_date
    }


# GET ALL WORKOUT PLANS
@router.get("/")
def get_plans(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user.id
    ).order_by(
        WorkoutPlan.scheduled_date
    ).all()


# GET UPCOMING WORKOUT PLANS
@router.get("/upcoming")
def upcoming_plans(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user.id,
        WorkoutPlan.scheduled_date >= date.today()
    ).order_by(
        WorkoutPlan.scheduled_date
    ).all()


# DELETE WORKOUT PLAN
@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.user_id == user.id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Workout plan not found"
        )

    db.delete(plan)
    db.commit()

    return {
        "message": "Workout plan deleted successfully"
    }
