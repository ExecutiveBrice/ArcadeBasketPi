import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "storage", "database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("storage/schema.sql", "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

def save_match(score, duration):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO matches (score, duration_seconds) VALUES (?, ?)",
        (score, duration)
    )

    conn.commit()
    conn.close()

def get_best_score():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(score) FROM matches")
    result = cursor.fetchone()[0]

    conn.close()
    return result if result else 0
