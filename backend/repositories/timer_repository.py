from models import Timer


class TimerRepository:
    def __init__(self, database):
        self.database = database

    def create(self, name, duration_seconds):
        connection = self.database.connect()
        try:
            cursor = connection.execute(
                """
                INSERT INTO timers (
                    name,
                    duration_seconds,
                    remaining_seconds,
                    status
                )
                VALUES (?, ?, ?, ?)
                """,
                (name, duration_seconds, duration_seconds, "Running"),
            )
            row = connection.execute(
                "SELECT * FROM timers WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            connection.commit()
            return Timer.from_row(row)
        finally:
            connection.close()

    def get_all(self):
        connection = self.database.connect()
        try:
            rows = connection.execute(
                "SELECT * FROM timers ORDER BY id"
            ).fetchall()
            return [Timer.from_row(row) for row in rows]
        finally:
            connection.close()