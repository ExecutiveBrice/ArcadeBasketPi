import sqlite3
from config import DB_PATH
import time

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS matchs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date INTEGER,
            score INTEGER,
            duration INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_match(score, duration):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO matchs (date, score, duration) VALUES (?, ?, ?)",
        (int(time.time()), score, duration)
    )
    conn.commit()
    conn.close()

def get_history(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT date, score, duration FROM matchs ORDER BY date DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows