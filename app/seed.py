from app.database import SessionLocal
from app.models import Badge

db = SessionLocal()

badges = [
    Badge(
        name="First Workout",
        description="Complete your first workout",
        icon="trophy"
    ),
    Badge(
        name="3 Day Streak",
        description="Complete workouts for 3 consecutive days",
        icon="flame"
    ),
    Badge(
        name="7 Day Streak",
        description="Complete workouts for 7 consecutive days",
        icon="star"
    ),
    Badge(
        name="Fitness Champion",
        description="Complete 30 workouts",
        icon="medal"
    )
]

for badge in badges:
    exists = db.query(Badge).filter(
        Badge.name == badge.name
    ).first()

    if not exists:
        db.add(badge)

db.commit()
db.close()

print("Badges inserted successfully")