import sqlite3
import os

DB_PATH = os.path.join("data", "simulation.db")

def init_db():
    os.makedirs("data", exist_ok=True)  # ensure folder exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            inbox_link TEXT NOT NULL UNIQUE,
            email_sent INTEGER DEFAULT 0,
            clicked INTEGER DEFAULT 0,
            submitted INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized at:", DB_PATH)

if __name__ == "__main__":
    init_db()
