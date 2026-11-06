import sqlite3

# Set this to the SAME database file your app uses in its database URL.
DATABASE_FILE = "fittrack.db"

with sqlite3.connect(DATABASE_FILE) as connection:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(users)")
    }

    if "password" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN password TEXT")
        print("Added users.password")
    else:
        print("users.password already exists")