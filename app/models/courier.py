from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Courier:
    name: str
    working_hours: timedelta
