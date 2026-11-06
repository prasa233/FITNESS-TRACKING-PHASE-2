
import sqlite3
import os

DB_NAME = "fittrack.db"

if not os.path.exists(DB_NAME):
    print("ERROR: fittrack.db not found!")
    print("Check your database file name and location.")
    exit()

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA table_info(goals)")
    columns = [row[1] for row in cursor.fetchall()]

    if not columns:
        print("ERROR: goals table does not exist!")
    else:
        print("Existing columns:", columns)

        if "start_date" not in columns:
            cursor.execute(
                "ALTER TABLE goals ADD COLUMN start_date DATE"
            )
            print("start_date added")

        if "target_date" not in columns:
            cursor.execute(
                "ALTER TABLE goals ADD COLUMN target_date DATE"
            )
            print("target_date added")

        if "status" not in columns:
            cursor.execute(
                "ALTER TABLE goals ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE'"
            )
            print("status added")

        conn.commit()
        print("Goals database migration completed!")

except Exception as e:
    conn.rollback()
    print("ERROR:", e)

finally:
    conn.close()
