class TimerService:
    def __init__(self, timer_repository):
        self.timer_repository = timer_repository

    def list_timers(self):
        return self.timer_repository.get_all()

    def create_timer(self, name, duration_seconds):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")

        if (
            isinstance(duration_seconds, bool)
            or not isinstance(duration_seconds, int)
            or duration_seconds <= 0
        ):
            raise ValueError(
                "duration_seconds must be a positive integer."
            )

        return self.timer_repository.create(
            name.strip(),
            duration_seconds,
        )