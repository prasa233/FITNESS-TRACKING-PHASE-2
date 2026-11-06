from sqlalchemy import inspect, text
from app.database import engine

inspector = inspect(engine)

if "workouts" not in inspector.get_table_names():
    print("Workouts table does not exist.")
else:
    columns = [
        column["name"]
        for column in inspector.get_columns("workouts")
    ]

    if "notes" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE workouts ADD COLUMN notes TEXT")
            )
        print("Successfully added notes column.")
    else:
        print("Notes column already exists.")