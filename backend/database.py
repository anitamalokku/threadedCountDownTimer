import sqlite3
from pathlib import Path

from models import Timer


DEFAULT_DATABASE_PATH = Path(__file__).resolve().with_name("timers.db")


def _connect(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS timers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0),
            remaining_seconds INTEGER NOT NULL CHECK (remaining_seconds >= 0),
            status TEXT NOT NULL
        )
        """
    )
    return connection


def create_timer(name, duration_seconds, database_path=DEFAULT_DATABASE_PATH):
    connection = _connect(database_path)
    try:
        cursor = connection.execute(
            """
            INSERT INTO timers (name, duration_seconds, remaining_seconds, status)
            VALUES (?, ?, ?, ?)
            """,
            (name, duration_seconds, duration_seconds, "Running"),
        )
        connection.commit()
        row = connection.execute(
            "SELECT * FROM timers WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return Timer.from_row(row)
    finally:
        connection.close()


def get_timers(database_path=DEFAULT_DATABASE_PATH):
    connection = _connect(database_path)
    try:
        rows = connection.execute("SELECT * FROM timers ORDER BY id").fetchall()
        return [Timer.from_row(row) for row in rows]
    finally:
        connection.close()