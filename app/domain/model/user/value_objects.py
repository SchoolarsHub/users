from dataclasses import dataclass


@dataclass(frozen=True)
class Fullname:
    firstname: str
    lastname: str
