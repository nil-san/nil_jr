import sqlite3
from datetime import datetime

DB_FILE = "mentions.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers (
    user_id INTEGER PRIMARY KEY,
    enabled INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mentions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id INTEGER,
    author_id INTEGER,
    channel_id INTEGER,
    guild_id INTEGER,
    message_url TEXT,
    timestamp TEXT
)
""")
conn.commit()

# DB helper functions
def is_active_subscriber(user_id: int) -> bool:
    cursor.execute(
        "SELECT enabled FROM subscribers WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    return row is not None and row[0] == 1

def add_subscriber(user_id: int):
    cursor.execute(
        """
        INSERT INTO subscribers (user_id, enabled)
        VALUES (?, 1)
        ON CONFLICT(user_id) DO UPDATE SET enabled = 1
        """,
        (user_id,)
    )
    conn.commit()

def remove_subscriber(user_id: int):
    cursor.execute(
        "DELETE FROM subscribers WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()

def enable_subscriber(user_id: int):
    cursor.execute(
        "UPDATE subscribers SET enabled = 1 WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()

def disable_subscriber(user_id: int):
    cursor.execute(
        "UPDATE subscribers SET enabled = 0 WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()