from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, synonym
from .database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
# ==========================================
# USER MODEL - PHASE 1
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    user_badges = relationship("UserBadge", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


    # Relationships
    workouts = relationship("Workout", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    streak = relationship("Streak", back_populates="user", uselist=False)
    user_badges = relationship("UserBadge", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


# ==========================================
# WORKOUT MODEL - PHASE 1 AND PHASE 2
# ==========================================

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    workout_name = Column(String(100), nullable=False)

    # Keep the original Phase 1 database column.
    category = Column(String(20), nullable=False)

    # Phase 2 API compatibility:
    # workout_type uses the existing category database column.
    workout_type = synonym("category")

    duration = Column(Integer, nullable=False)

    calories_burned = Column(Float, default=0)

    workout_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Phase 2 field
    notes = Column(Text, nullable=True)

    # Relationship
    user = relationship("User", back_populates="workouts")

# ==========================================
# WORKOUT PLANS - PHASE 2 MODULE 7
# ==========================================

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    scheduled_date = Column(Date, nullable=False)
# ==========================================
# PROGRESS MODEL - PHASE 1
# ==========================================

class Progress(Base):
    __tablename__ = "progress"

    __table_args__ = (
        UniqueConstraint("user_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    total_workouts: Mapped[int] = mapped_column(
        Integer, default=0
    )

    total_calories: Mapped[float] = mapped_column(
        Float, default=0
    )

    date: Mapped[date] = mapped_column(Date)

    user = relationship("User", back_populates="progress_records")


# ==========================================
# GOAL MODEL - PHASE 1 / PHASE 2
# ==========================================

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    goal_type = Column(String(100), nullable=False)

    target_value = Column(Float, nullable=False)

    current_value = Column(Float, default=0)

    start_date = Column(Date, nullable=False)

    target_date = Column(Date, nullable=False)

    deadline = Column(Date, nullable=False)

    status = Column(String(30), default="ACTIVE")

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship("User", back_populates="goals")


# ==========================================
# EXERCISE LIBRARY - PHASE 2 MODULE 8
# ==========================================

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    category = Column(String(50), nullable=False)

    description = Column(Text)

    duration = Column(Integer, nullable=False)


# ==========================================
# STREAK TRACKING - PHASE 2 MODULE 10
# ==========================================

class Streak(Base):
    __tablename__ = "streak"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    current_streak = Column(Integer, default=0)

    longest_streak = Column(Integer, default=0)

    last_workout_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="streak")


# ==========================================
# ACHIEVEMENT BADGES - PHASE 2 MODULE 11
# ==========================================

class AchievementBadge(Base):
    __tablename__ = "achievement_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    badge_type = Column(String(100), nullable=False)
    icon = Column(String(100), nullable=True)


# ==========================================
# BADGES
# ==========================================

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    icon = Column(String(255), nullable=True)

    user_badges = relationship(
        "UserBadge",
        back_populates="badge",
        cascade="all, delete-orphan"
    )


# ==========================================
# USER BADGES
# ==========================================

class UserBadge(Base):
    __tablename__ = "user_badges"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), primary_key=True)

    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")
# ==========================================
# NOTIFICATIONS - PHASE 2
# ==========================================

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    title: Mapped[str] = mapped_column(String(120))

    message: Mapped[str] = mapped_column(String(500))

    is_read: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user = relationship("User", back_populates="notifications")