from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ExperiencesPeriod:
    start_date: date
    end_date: date
