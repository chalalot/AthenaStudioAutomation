import sqlite3
from datetime import datetime
import os

DB_FILE = "task_log.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            status TEXT,
            timestamp TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_task(task_id, status, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (task_id, status, timestamp, message) VALUES (?, ?, ?, ?)",
        (task_id, status, datetime.now().isoformat(), message)
    )
    conn.commit()
    conn.close()
