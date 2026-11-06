from pydantic import BaseModel, Field
from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

# User Registration
class RegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


# User Login
class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# User Response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


# Authentication Token
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
# WORKOUT PLANS

class WorkoutPlanCreate(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_date: date


class WorkoutPlanResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    scheduled_date: date

    class Config:
        from_attributes = True
# Create Workout
class WorkoutCreate(BaseModel):
    workout_name: str
    workout_type: str
    duration: int
    calories_burned: int = 0
    workout_date: date
    notes: Optional[str] = None



# Update Workout
class WorkoutUpdateSchema(BaseModel):
    workout_name: Optional[str] = None
    workout_type: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[float] = None
    workout_date: Optional[date] = None
    notes: Optional[str] = None


# Workout Response
class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    workout_name: str
    workout_type: str
    duration: int
    calories_burned: int
    workout_date: date
    notes: Optional[str] = None

    class Config:
        from_attributes = True
class WorkoutSchema(BaseModel):
    workout_name: str
    workout_type: str
    duration: int
    calories_burned: float = 0
    workout_date: date
    notes: Optional[str] = None


class WorkoutUpdateSchema(BaseModel):
    workout_name: Optional[str] = None
    workout_type: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[float] = None
    workout_date: Optional[date] = None
    notes: Optional[str] = None


class WorkoutResponseSchema(WorkoutSchema):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# EXERCISES

class ExerciseCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    duration: int = Field(gt=0)


class ExerciseResponse(ExerciseCreate):
    id: int

    class Config:
        from_attributes = True


# BADGES

class BadgeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]

    class Config:
        from_attributes = True
# Create Goal
class GoalSchema(BaseModel):
    goal_type: str = Field(..., min_length=2)
    target_value: float = Field(..., gt=0)
    current_value: float = Field(default=0, ge=0)
    start_date: date
    target_date: date
    status: str = "ACTIVE"


# Update Goal
class GoalUpdateSchema(BaseModel):
    goal_type: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    status: Optional[str] = None


# Goal Response
class GoalResponseSchema(BaseModel):
    id: int
    user_id: int
    goal_type: str
    target_value: float
    current_value: float
    start_date: date
    target_date: date
    status: str

    class Config:
        from_attributes = True
class GoalSchema(BaseModel):
    goal_type: str
    target_value: float
    current_value: float = 0
    start_date: date
    target_date: date

class AchievementBadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    badge_type: str
    icon: Optional[str] = None


class AchievementBadgeResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    badge_type: str
    icon: Optional[str] = None

    class Config:
        from_attributes = True