from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Timer:
    id: int
    name: str
    duration_seconds: int
    remaining_seconds: int
    status: str

    @classmethod
    def from_row(cls, row):
        return cls(**dict(row))

    def to_dict(self):
        return asdict(self)
