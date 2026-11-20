import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = Path(__file__).resolve().with_name("timers.db")


class Database:
    def __init__(self, database_path=DEFAULT_DATABASE_PATH):
        self.database_path = Path(database_path)

    def connect(self):
        connection = sqlite3.connect(self.database_path)
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