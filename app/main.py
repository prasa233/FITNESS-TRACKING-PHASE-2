

from datetime import date, datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import achievement_badges
from sqlalchemy.orm import Session

from dotenv import load_dotenv

load_dotenv()

from .database import Base, engine, get_db

from . import models, schemas

from .security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from .routers import (
    workout_plans,
    exercises,
    progress,
    streaks,
    badges,
    dashboard
)



# ---------------------------------
# DATABASE INITIALIZATION
# ---------------------------------



Base.metadata.create_all(bind=engine)


# ---------------------------------
# FASTAPI APPLICATION
# ---------------------------------

app = FastAPI(
    title="FitTrack Fitness Platform",
    description="Phase 1 and Phase 2 Fitness Tracking API",
    version="2.0.0"
)



# ---------------------------------
# CORS CONFIGURATION
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Welcome to FitTrack API",
        "status": "Running"
    }


# =================================
# MODULE 1: USER AUTHENTICATION
# =================================
@app.post("/auth/register", status_code=201)
def register(
    data: schemas.RegisterSchema,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == data.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered.",
        )

    new_user = models.User(
        username=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        created_at=datetime.utcnow(),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed. Please try again.",
        )

    return {
        "message": "Registration successful",
        "user_id": new_user.id,
        "name": new_user.username,
        "email": new_user.email,
    }


@app.post("/auth/login")
def login(
    data: schemas.LoginSchema,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == data.email)
        .first()
    )

    if user is None or not verify_password(
        data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@app.get("/auth/me")
def get_profile(
    user: models.User = Depends(get_current_user),
):
    return {
        "id": user.id,
        "name": user.username,
        "email": user.email,
    }

# =================================
# MODULE 2: WORKOUT MANAGEMENT
# =================================

@app.post("/workouts")
def create_workout(
    data: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    workout = models.Workout(
        user_id=current_user.id,
        workout_name=data.workout_name,
        workout_type=data.workout_type,
        duration=data.duration,
        calories_burned=data.calories_burned,
        workout_date=data.workout_date,
        notes=data.notes
    )

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout

@app.get("/workouts")
def get_workouts(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    return db.query(models.Workout).filter(
        models.Workout.user_id == user.id
    ).order_by(
        models.Workout.workout_date.desc()
    ).all()


@app.put("/workouts/{workout_id}")
def edit_workout(
    workout_id: int,
    data: schemas.WorkoutSchema,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id,
        models.Workout.user_id == user.id
    ).first()

    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    old_date = workout.workout_date

    for key, value in data.model_dump().items():
        setattr(workout, key, value)

    db.commit()
    db.refresh(workout)

    update_daily_progress(db, user.id, old_date)

    if old_date != workout.workout_date:
        update_daily_progress(
            db, user.id, workout.workout_date
        )

    return {
        "message": "Workout updated successfully"
    }


@app.delete("/workouts/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id,
        models.Workout.user_id == user.id
    ).first()

    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    workout_date = workout.workout_date

    db.delete(workout)
    db.commit()

    update_daily_progress(
        db,
        user.id,
        workout_date
    )

    return {
        "message": "Workout deleted successfully"
    }


# =================================
# MODULE 3: DAILY PROGRESS TRACKING
# =================================


def update_daily_progress(
    db: Session,
    user_id: int,
    selected_date: date
):

    workouts = db.query(models.Workout).filter(
        models.Workout.user_id == user_id,
        models.Workout.workout_date == selected_date
    ).all()

    total_workouts = len(workouts)

    total_calories = sum(
        workout.calories_burned
        for workout in workouts
    )

    progress = db.query(models.Progress).filter(
        models.Progress.user_id == user_id,
        models.Progress.date == selected_date
    ).first()

    if not progress:
        progress = models.Progress(
            user_id=user_id,
            date=selected_date
        )
        db.add(progress)

    progress.total_workouts = total_workouts
    progress.total_calories = total_calories

    db.commit()
    db.refresh(progress)

    return progress


@app.get("/progress/daily")
def daily_progress(
    selected_date: date | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    selected_date = selected_date or date.today()

    progress = update_daily_progress(
        db,
        user.id,
        selected_date
    )

    return {
        "date": progress.date,
        "total_workouts": progress.total_workouts,
        "total_calories": progress.total_calories
    }


@app.get("/progress")
def progress_history(
    days: int = 7,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    if days < 1 or days > 365:
        raise HTTPException(
            status_code=422,
            detail="Days must be between 1 and 365"
        )

    start_date = date.today() - timedelta(days=days - 1)

    result = []

    for offset in range(days):
        current_date = start_date + timedelta(days=offset)

        progress = update_daily_progress(
            db,
            user.id,
            current_date
        )

        result.append({
            "date": progress.date,
            "total_workouts": progress.total_workouts,
            "total_calories": progress.total_calories
        })

    return result


# =================================
# MODULE 4: GOAL SETTING SYSTEM
# =================================
@app.post("/goals", status_code=201)
def create_goal(
    data: schemas.GoalSchema,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        goal = models.Goal(
            user_id=current_user.id,
            goal_type=data.goal_type,
            target_value=data.target_value,
            current_value=data.current_value,
            start_date=data.start_date,
            target_date=data.target_date,
            deadline=data.target_date,
            status="ACTIVE",
            created_at=datetime.utcnow()
        )

        db.add(goal)
        db.commit()
        db.refresh(goal)

        return {
            "message": "Goal created successfully",
            "goal": goal
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unable to create goal: {str(e)}"
        )



@app.get("/goals")
def get_goals(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    return db.query(models.Goal).filter(
        models.Goal.user_id == user.id
    ).all()


@app.patch("/goals/{goal_id}")
def update_goal(
    goal_id: int,
    current_value: float,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user.id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if current_value < 0:
        raise HTTPException(
            status_code=422,
            detail="Current value cannot be negative"
        )

    goal.current_value = current_value

    goal.status = (
        "COMPLETED"
        if current_value >= goal.target_value
        else "IN_PROGRESS"
    )

    db.commit()
    db.refresh(goal)

    if goal.status == "COMPLETED":
        db.add(models.Notification(
            user_id=user.id,
            title="Goal completed!",
            message=f"You completed your {goal.goal_type} goal."
        ))
        db.commit()

    return goal


@app.delete("/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user.id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    db.delete(goal)
    db.commit()

    return {"message": "Goal deleted successfully"}


# =================================
# MODULE 5: REPORTS AND ANALYTICS
# =================================


@app.get("/reports/weekly")
def weekly_report(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    start_date = date.today() - timedelta(days=6)

    workouts = db.query(models.Workout).filter(
        models.Workout.user_id == user.id,
        models.Workout.workout_date >= start_date
    ).all()

    total_calories = sum(
        workout.calories_burned
        for workout in workouts
    )

    total_duration = sum(
        workout.duration
        for workout in workouts
    )

    return {
        "total_workouts": len(workouts),
        "total_calories": total_calories,
        "total_duration": total_duration,
        "by_category": {
            category: sum(
                1 for workout in workouts
                if workout.category == category
            )
            for category in ["Cardio", "Strength", "Yoga"]
        }
    }


@app.get("/reports/monthly")
def monthly_report(
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    today = date.today()
    year = year or today.year
    month = month or today.month

    if month < 1 or month > 12:
        raise HTTPException(
            status_code=422,
            detail="Month must be between 1 and 12"
        )

    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    workouts = db.query(models.Workout).filter(
        models.Workout.user_id == user.id,
        models.Workout.workout_date >= start_date,
        models.Workout.workout_date < end_date
    ).all()

    return {
        "year": year,
        "month": month,
        "total_workouts": len(workouts),
        "total_calories": sum(
            w.calories_burned for w in workouts
        ),
        "total_duration": sum(
            w.duration for w in workouts
        )
    }


# =================================
# MODULE 6: NOTIFICATIONS SYSTEM
# =================================


@app.get("/notifications")
def get_notifications(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    return db.query(models.Notification).filter(
        models.Notification.user_id == user.id
    ).order_by(
        models.Notification.created_at.desc()
    ).all()


@app.patch("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == user.id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read"
    }


@app.post("/notifications/reminder", status_code=201)
def create_daily_reminder(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):

    reminder = models.Notification(
        user_id=user.id,
        title="Daily Workout Reminder",
        message="Stay active! Complete your workout today."
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return {
        "message": "Daily reminder created",
        "notification_id": reminder.id
    }
app.include_router(workout_plans.router)
app.include_router(exercises.router)
app.include_router(progress.router)
app.include_router(streaks.router)
app.include_router(badges.router)
app.include_router(dashboard.router)
app.include_router(achievement_badges.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "FitTrack Phase 2 Backend Running"
    }